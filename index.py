import numpy as np
import random

# parâmetros base
n = 30                       # tamanho da grade (NxN)
proporcao_inicial = 0.2      # quantidade inicial de alunos atentos
influencia_vizinhos = 3      # influência ds vizinhos
Ts = 5                       # tempo de saturação
pd = 0.3                     # probabilidade de reinício com intervenção docente
iteracoes = 20               # número de iterações (1 aula)

# geração da grade NxN
grade = np.zeros((n, n), dtype=int)

# Contador de tempo de atenção (τ)
tempo_atencao = np.zeros((n, n), dtype=int)

# geração alunos atentos inicial
num_estado_1 = int(proporcao_inicial * n * n)
indices = np.random.choice(n * n, num_estado_1)

for posicao_grade in indices:
    i = posicao_grade // n
    j = posicao_grade % n
    grade[i, j] = 1

# contagem de vizinhos atentos (moore)

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

    # registro das métricas do sistema (global)

    historico_0 = []
    historico_1 = []
    historico_2 = []
    historico_grades = []

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