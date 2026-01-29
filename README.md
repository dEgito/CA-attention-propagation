## Simulação da Propagação da Atenção em Sala de Aula

**Danielly Egito de Moura¹**  
¹ Departamento de Estatística e Informática Universidade Federal Rural de Pernambuco (UFRPE) – Recife, PE – Brasil  
¹danielly.egitom@ufrpe.br 

**Resumo:** *A atenção desempenha um papel central no processo de aprendizagem, sendo influenciada por interações sociais, limites cognitivos e mediação docente. Este estudo propõe um modelo baseado em autômatos celulares para simular a dinâmica da atenção em uma turma de estudantes, considerando a interação entre pares e a influência do professor. A implementação computacional foi realizada em Python, permitindo a simulação da evolução temporal do sistema sob diferentes configurações. Os resultados indicam que a interação entre alunos, isoladamente, não sustenta o engajamento coletivo ao longo do tempo. A inserção do professor como agente externo contribui para a estabilidade do sistema e manutenção da atenção, evidenciando a relevância da mediação docente.*

## Descrição do repositório:

- Pasta de Resultados:
  Pasta contendo as imagens geradas pelas simulações.
  Cada experimento apresenta:
  - o gráfico de evolução temporal dos estados de atenção;
  - a visualização final da grade do autômato celular.

- Artigo final:
  Versão final do artigo que descreve o modelo, metodologia e a análise dos resultados obtidos nas simulações.

- Index-Professor.py:
  Versão do código que implementa a lógica de influência docente.

- Index.py:
  Versão do código sem a lógica de influência docente, focada apenas na interação entre pares.

- Pseudocódigo.txt:
  Representação abstrata da lógica do modelo.


## Parâmetros do modelo:

Todos as versões presentes no repositório utilizam os arranjo estável de parámetros definidos da seguinte maneira:

- Tamanho da grade (n) = 20
- Proporção inicial de alunos atentos = 0.2
- Número mínimo de vizinhos atentos para engajar = 3
- Tempo máximo até a saturação = 5
- Probabilidade de retomar ao estado neutro (pd) = 0.3
- Iterações = 20
