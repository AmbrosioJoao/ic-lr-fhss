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

"*********Anotações*********"

#Primeira Curva (A):
    #Fixado: 1/3 de taxa
    
#Segunda Curva (B):
    #Fixado: 1/2 de taxa

#Terceira Curva (C):
    #Fixado: 2/3 de taxa
    
#Quarta Curva (D):
    #Fixado: 5/6 de taxa 
    
#ORDENADO DO MENOR PARA O MAIOR AOI

estilos = ['-', '--', '-.', ':', (0, (3, 5, 1, 5))]  # Diferentes estilos de linha
cores = ['blue', 'green', 'red', 'orange', 'magenta']  # Cores para cada curva
marcadores = ['o', 's', '^', 'd', 'x']  # Diferentes tipos de marcadores

"***************************"

# Parâmetros da simulação
nNodes_points = 20
nNodes_min = 1000
nNodes_max = 15000
nNodes = np.linspace(nNodes_min, nNodes_max, nNodes_points, dtype=int)//8
loops = 1

# Função para rodar simulações
def run_simulation(nNodes, loops, param_name, param_values):
    results = {code: {'success': [], 'goodput': [], 'AoI': []} for code in ['1/3', '1/2', '2/3', '5/6']}
    
    for value in param_values:
        for code in results.keys():
            payload_size = value if param_name == 'payload_size' else 16  # Definir um valor padrão
            s = Settings(number_nodes=value if param_name == 'number_nodes' else 80000//8, code=code, 
                         payload_size=payload_size)
            sim_results = Parallel(n_jobs=8)(delayed(run_sim)(s, seed=seed) for seed in range(loops))
            
            results[code]['success'].append(np.mean(sim_results, 0)[0])
            results[code]['goodput'].append(np.mean(sim_results, 0)[1])
            results[code]['AoI'] = (np.mean(sim_results, 0)[3])
            
        print(value*8)
    
    return results

# Rodando simulação para diferentes quantidades de dispositivos
start = time.perf_counter()
nodes_results = run_simulation(nNodes, loops, 'number_nodes', nNodes)
print(f"Simulação 1 concluída em {time.perf_counter()-start} segundos.")

# Rodando simulação para diferentes tamanhos de payload
pNodes_points = 20
pNodes_min = 32  # 8*4 P.S
pNodes_max = 160 # 8*20 P.S
pNodes = np.linspace(pNodes_min, pNodes_max, pNodes_points, dtype=int)//8
start = time.perf_counter()
payload_results = run_simulation(pNodes, loops, 'payload_size', pNodes)
print(f"Simulação 2 concluída em {time.perf_counter()-start} segundos.")

# Função para plotar resultados
def plot_results(x_values, results, xlabel):
    with plt.style.context(['science', 'ieee', 'no-latex']):
        fig, ax = plt.subplots()
        ax.xaxis.set_major_formatter(EngFormatter())
        ax.set(ylabel='AoI médio', xlabel=xlabel)
        
        for idx, (code, data) in enumerate(results.items()):
            ax.plot(x_values, (np.array(data['AoI'])*x_values)/1000000, linestyle=estilos[idx], 
                    color=cores[idx], marker=marcadores[idx], markersize=1, markevery=2, label=f'{code} C.R.')
        
        ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.8, edgecolor='black')
        ax.grid(ls='--', color='lightgray')
        ax.autoscale(tight=True)
        ax.set_ylim(bottom=0)
        plt.tight_layout()
        plt.show()
        plt.close()

# Plotando resultados para quantidade de dispositivos
plot_results(nNodes, nodes_results, 'Número de dispositivos')

# Plotando resultados para tamanhos de payload
plot_results(pNodes, payload_results, 'Tamanho do Payload')
