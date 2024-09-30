"Bibliotecas para os gráficos"
from lrfhss.run import *
import time
from joblib import Parallel, delayed
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import pickle
import pandas as pd
from matplotlib.ticker import EngFormatter
import scienceplots


"************GRÁFICOS****************"
# 'Pontos' de nós (each simulation takes one different)
nNodes_points = 10
# Quantidade mínima de nós
nNodes_min = 1000
# Quantidade mínima de nós
nNodes_max = 150000
# O número de nós é divido por 8, "as we are simulating one of the 8 grid" "<- perguntar."
# Como eles são selecionados aleatoriamente, é uma boa aproximação considerar apenas um deles, e decairá conforme o tempo.
# No final, multiplicamos esse vetor por 8 se quisermos considerar a capacidade total da tecnologia.

nNodes = np.linspace(nNodes_min, nNodes_max, nNodes_points, dtype=int)//8

# Número de loops
loops = 1

start = time.perf_counter()


# Vetores de sucesso ajustado, cada gráfico precisa de 3 vetores success e 3 vetores goodput
success = []
goodput = []
total_headers = []
total_fragments = []
total_ToA = []

# Para cada número de nodes_point, roda a simulação "loops" vezes

for n in nNodes:
    # Variaveis para cada gráfico:
    settings_scenario1 = Settings(number_nodes=n, headers=3)

    # Resultados do gráfico:
    results = Parallel(n_jobs=8)(delayed(run_sim)(
        settings_scenario1, seed=seed) for seed in range(0, loops))

    # Ajustar sucessos para o gráfico A:
    success.append(np.mean(results, 0)[0])
    goodput.append(np.mean(results, 0)[2]*np.mean(results, 0)[0])

    # Aqui nós recuperamos da simulação o total de headers e fragmentos calculados no arquivo run.py. Também multiplicamos este total pelas especificações de
    # tempo de cada header e tempo de cada fragmento na linha 58 que vai resultar no ToA total.
    total_headers.append(np.mean(results, 0)[3])
    total_fragments.append(np.mean(results, 0)[4])

    # Dividido por 3600 pois o total de headers e fragmentos corresponde a todo tempo de simulação: 3600s. Estamos interessados em uma análise por segundo.
    # np.mean(results,0)[3].astype(float)

    # Para o bar plot funcionar tive que "tratar" os np.array para list colocando este [0] ao final de: (np.mean(results,0)[3])[0]
    total_ToA.append((((np.mean(results, 0)[3])[0]*settings_scenario1.header_duration+(
        np.mean(results, 0)[4])[0]*settings_scenario1.payload_duration)/3600))
    ######

    print(n*8)

print("The simulation lasted {time.perf_counter()-start} seconds.")

f_x = EngFormatter()

with plt.style.context(['science', 'ieee', 'no-latex']):
    # Make a random dataset:
    height = total_ToA
    y_pos = np.arange(len(nNodes))

    # Create bars
    plt.bar(y_pos, height)

    # Create names on the x-axis
    plt.xticks(y_pos, height)

    # Show graphic
    plt.show()
