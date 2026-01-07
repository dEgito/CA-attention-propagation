import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import animation

# ===============================
# Parâmetros do modelo
# ===============================

n = 20                       # tamanho da grade (NxN)
proporcao_inicial = 0.2      # fração inicial de alunos atentos
theta = 3                    # limiar de influência social
Ts = 5                       # tempo de saturação (iterações)
pd = 0.3                     # probabilidade de reinício
iteracoes = 20               # número de iterações
raio_prof = 1                # raio de influência do professor

# ===============================
# Inicialização da grade
# ===============================

# Estados: 0 = desatenção | 1 = atenção | 2 = saturação
grade = np.zeros((n, n), dtype=int)
tau = np.zeros((n, n), dtype=int)

# Inicializar alunos atentos
num_estado_1 = int(proporcao_inicial * n * n)
indices = np.random.choice(n * n, num_estado_1, replace=False)

for idx in indices:
    i, j = divmod(idx, n)
    grade[i, j] = 1

# ===============================
# Inicialização do professor
# ===============================

prof_i, prof_j = n // 2, n // 2
historico_prof = []

# ===============================
# Funções auxiliares
# ===============================

def contar_atentos(grade, i, j):
    contagem = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n:
                if grade[ni, nj] == 1:
                    contagem += 1
    return contagem

def influencia_professor(grade, pi, pj, raio):
    for i in range(n):
        for j in range(n):
            if max(abs(i - pi), abs(j - pj)) <= raio:
                grade[i, j] = 1
                tau[i, j] = 0

def mover_professor(pi, pj):
    movimentos = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1]
                  if not (di == 0 and dj == 0)]
    di, dj = random.choice(movimentos)
    ni, nj = pi + di, pj + dj
    if 0 <= ni < n and 0 <= nj < n:
        return ni, nj
    return pi, pj

def grade_para_scatter(grade):
    xs, ys, cores = [], [], []
    for i in range(n):
        for j in range(n):
            xs.append(j)
            ys.append(i)
            if grade[i, j] == 0:
                cores.append('lightgray')
            elif grade[i, j] == 1:
                cores.append('green')
            else:
                cores.append('red')
    return xs, ys, cores

# ===============================
# Estruturas de registro
# ===============================

historico_0 = []
historico_1 = []
historico_2 = []
historico_grades = []

# ===============================
# Loop principal do autômato
# ===============================

for t in range(iteracoes):
    nova_grade = grade.copy()

    for i in range(n):
        for j in range(n):
            estado = grade[i, j]
            A = contar_atentos(grade, i, j)

            if estado == 0 and A >= theta:
                nova_grade[i, j] = 1
                tau[i, j] = 0

            elif estado == 1:
                tau[i, j] += 1
                if tau[i, j] >= Ts:
                    nova_grade[i, j] = 2
                    tau[i, j] = 0

            elif estado == 2:
                if random.random() < pd:
                    nova_grade[i, j] = 0

    # Atualização do professor
    prof_i, prof_j = mover_professor(prof_i, prof_j)
    influencia_professor(nova_grade, prof_i, prof_j, raio_prof)

    # Atualização síncrona
    grade = nova_grade

    # Registro
    historico_0.append(np.sum(grade == 0))
    historico_1.append(np.sum(grade == 1))
    historico_2.append(np.sum(grade == 2))
    historico_grades.append(grade.copy())
    historico_prof.append((prof_i, prof_j))

# ===============================
# Relatório final
# ===============================

print("Última iteração:")
print("Desatentos:", historico_0[-1])
print("Atentos:", historico_1[-1])
print("Saturados:", historico_2[-1])

# ===============================
# Gráfico temporal
# ===============================

plt.figure(figsize=(8, 5))
plt.plot(historico_0, label='Desatenção')
plt.plot(historico_1, label='Atenção')
plt.plot(historico_2, label='Saturação')
plt.xlabel("Iterações")
plt.ylabel("Número de estudantes")
plt.title("Evolução dos estados de atenção")
plt.legend()
plt.grid(True)
plt.show()

# ===============================
# Animação com esferas
# ===============================

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1, n)
ax.set_ylim(-1, n)
ax.set_aspect('equal')
ax.invert_yaxis()
ax.axis('on')

xs, ys, cores = grade_para_scatter(historico_grades[0])
alunos_plot = ax.scatter(xs, ys, c=cores, s=60)
prof_plot = ax.scatter([], [], c='black', s=140, marker='*')

def atualizar(frame):
    xs, ys, cores = grade_para_scatter(historico_grades[frame])
    alunos_plot.set_offsets(np.c_[xs, ys])
    alunos_plot.set_color(cores)

    pi, pj = historico_prof[frame]
    prof_plot.set_offsets([[pj, pi]])

    ax.set_title(f"Iteração {frame}")
    return alunos_plot, prof_plot

ani = animation.FuncAnimation(
    fig,
    atualizar,
    frames=len(historico_grades),
    interval=300,
    repeat=False
)

plt.show()
