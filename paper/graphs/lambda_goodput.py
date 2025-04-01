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

estilos = ['-', '--', '-.', ':', (0, (3, 5, 1, 5))]  # Diferentes estilos de linha
cores = ['blue', 'green', 'red', 'orange', 'magenta']  # Cores para cada curva
marcadores = ['o', 's', '^', 'd', 'x']  # Diferentes tipos de marcadores



"***************************"

nLambda_points = 15
nLambda_min = 600
nLambda_max = 5600

nLambda = np.linspace(nLambda_min, nLambda_max, nLambda_points, dtype=int)

nNodes = 80000//8
#Number of simulation loops for each configuration.
loops = 5

start = time.perf_counter()
success_case1 = []
goodput_case1 = []
AoI_case1 = []

success_case2 = []
goodput_case2 = []
AoI_case2 = []

success_case3 = []
goodput_case3 = []
AoI_case3 = []

success_case4 = []
goodput_case4 = []
AoI_case4 = []

#For each number of nodes point, run the simulation "loops" times
for n in nLambda:
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = nNodes, code = '5/6', headers=1, traffic_param={'average_interval': n})
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_1 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.
    success_case1.append(np.mean(results_1,0)[0])
    goodput_case1.append(np.mean(results_1,0)[1])
    AoI_case1.append(np.mean(results_1,0)[3])
    
    "***********************************"
 
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = nNodes, code = '2/3', headers=2, traffic_param={'average_interval': n})
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_2 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.

    success_case2.append(np.mean(results_2,0)[0])
    goodput_case2.append(np.mean(results_2,0)[1])
    AoI_case2.append(np.mean(results_2,0)[3])

    "***********************************"
 
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = nNodes, code = '1/2', headers=2, traffic_param={'average_interval': n})
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_3 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.

    success_case3.append(np.mean(results_3,0)[0])
    goodput_case3.append(np.mean(results_3,0)[1])
    AoI_case3.append(np.mean(results_3,0)[3])

    "***********************************"
 
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = nNodes, code = '1/3', headers=3, traffic_param={'average_interval': n})
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_4 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.

    success_case4.append(np.mean(results_4,0)[0])
    goodput_case4.append(np.mean(results_4,0)[1])
    AoI_case4.append(np.mean(results_4,0)[3])    

    print(n*8)

print(f"Case 1: Goodput: {goodput_case1} - AoI: {AoI_case1}")
print(f"Case 2: Goodput: {goodput_case2} - AoI: {AoI_case2}")
print(f"Case 3: Goodput: {goodput_case3} - AoI: {AoI_case3}")
print(f"Case 4: Goodput: {goodput_case4} - AoI: {AoI_case4}")


print(f"The simulation lasted {time.perf_counter()-start} seconds.")


with plt.style.context(['science', 'ieee', 'no-latex']):
    pparam = dict(ylabel='Goodput', xlabel='Taxa de pacotes')
    fig, ax = plt.subplots()

    # Adicionando curvas com diferentes estilos e cores, ajustando tamanho e espaçamento dos marcadores
    ax.plot(nLambda, goodput_case4, linestyle=estilos[0], color=cores[0], marker=marcadores[0], 
            markersize=4, markevery=4, label='H:3 - CR:1/3')  # Exibe marcador a cada 5 pontos
    
    ax.plot(nLambda, goodput_case3, linestyle=estilos[1], color=cores[1], marker=marcadores[1], 
            markersize=4, markevery=4, label='H:2 - CR:1/2')
    
    ax.plot(nLambda, goodput_case2, linestyle=estilos[2], color=cores[2], marker=marcadores[2], 
            markersize=4, markevery=4, label='H:2 - CR:2/3')
    
    ax.plot(nLambda, goodput_case1, linestyle=estilos[3], color=cores[3], marker=marcadores[3], 
            markersize=4, markevery=4, label='H:1 - CR:5/6')
    
   

    # Melhorias visuais
    leg = ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.8, edgecolor='black')
    ax.grid(ls='--', color='lightgray', alpha=0.6)
    ax.autoscale(tight=True)
    ax.set(**pparam)
    ax.set_ylim(bottom=0)  # Ajuste conforme necessário
    plt.gca().xaxis.set_major_formatter(EngFormatter(unit='', places=0))
    plt.gca().yaxis.set_major_formatter(EngFormatter(unit='', places=0))
   
    # Título com um tamanho maior
    # ax.set_title('Goodput varying the payload size (Fixed 50k Nodes)', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.show()


