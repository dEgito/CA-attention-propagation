import numpy as np
import random

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import animation

# parâmetros base
n = 20                       # tamanho da grade (NxN)
proporcao_inicial = 0.2      # quantidade inicial de alunos atentos
influencia_vizinhos = 3      # influência ds vizinhos
Ts = 5                       # tempo de saturação
pd = 0.3                     # probabilidade de reinício com intervenção docente
iteracoes = 20               # número de iterações (1 aula)

passos_moore = [(-1, -1), (-1, 0), (-1, 1),
                ( 0, -1),          ( 0, 1),
                ( 1, -1), ( 1, 0), ( 1, 1)]


# geração da grade NxN
grade = np.zeros((n, n), dtype=int)

# Contador de tempo de atenção (τ)
tempo_atencao = np.zeros((n, n), dtype=int)

# geração alunos atentos inicial
num_estado_1 = int(proporcao_inicial * n * n)
indices = np.random.choice(n * n, num_estado_1, replace=False)

for posicao_grade in indices:
    i = posicao_grade // n
    j = posicao_grade % n
    grade[i, j] = 1

# contagem de vizinhos atentos (moore)

def contar_atentos(grade, i, j):
    contagem = 0
    for di, dj in passos_moore:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < n:
            if grade[ni, nj] == 1:
                contagem += 1
    return contagem


# registro das métricas do sistema (global)

historico_0 = []
historico_1 = []
historico_2 = []
historico_grades = []
# loop de iterações e transições do autômato

for t in range(iteracoes):
    nova_grade = grade.copy()

    for i in range(n):
        for j in range(n):
            estado_atual = grade[i, j]
            A = contar_atentos(grade, i, j)

            # Regra 0 -> 1 (desatenção → atenção)
            if estado_atual == 0:
                if A >= influencia_vizinhos:
                    nova_grade[i, j] = 1
                    tempo_atencao[i, j] = 0

            # Regra 1 -> 2 (atenção → saturação)
            elif estado_atual == 1:
                tempo_atencao[i, j] += 1
                if tempo_atencao[i, j] >= Ts:
                    nova_grade[i, j] = 2
                    tempo_atencao[i, j] = 0

            # Regra 2 -> 0 (saturação → desatenção)
            elif estado_atual == 2:
                tempo_atencao[i, j] = 0
                if random.random() < pd:
                    nova_grade[i, j] = 0

    # atualização síncrona das células
    grade = nova_grade

    # métricas globais
    historico_0.append(np.sum(grade == 0))
    historico_1.append(np.sum(grade == 1))
    historico_2.append(np.sum(grade == 2))
    historico_grades.append(grade.copy()) # estado da grade (espacial)

# resultado da última iteração

print("Última iteração:")
print("Desatentos:", historico_0[-1])
print("Atentos:", historico_1[-1])
print("Saturados:", historico_2[-1])


###########################
## VISUALIZAÇÃO DO PROCESSO

# resultado da última iteração

cmap = ListedColormap(['lightgray', 'green', 'red'])

plt.figure(figsize=(6, 6))
plt.imshow(grade, cmap=cmap)
plt.title("Resultado da última iteração")
plt.axis('off')
plt.show()

# gráfico de linha: variação dos estados dos alunos x iterações

plt.figure(figsize=(8, 5))
plt.plot(historico_0, label='Desatenção (0)')
plt.plot(historico_1, label='Atenção (1)')
plt.plot(historico_2, label='Saturação (2)')
plt.xlabel("Iterações (tempo)")
plt.ylabel("Número de estudantes")
plt.title("Evolução dos estados ao longo das iterações")
plt.grid(True)
plt.show()

# animação da evolução

fig, ax = plt.subplots(figsize=(6, 6))
img = ax.imshow(historico_grades[0], cmap=cmap)
ax.axis('off')

def atualizar(frame):
    img.set_array(historico_grades[frame])
    ax.set_title(f"Iteração {frame}")

    return img, 

ani = animation.FuncAnimation(
    fig,
    atualizar,
    frames=len(historico_grades),
    interval=150,
    repeat=False
)

plt.show()