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

nPayload_points = 5
nPayload_min = 10
nPayload_max = 50

nPayload = np.linspace(nPayload_min, nPayload_max, nPayload_points, dtype=int)
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
for n in nPayload:
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = nNodes, code = '5/6', headers=1, payload_size=n)
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_1 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.
    success_case1.append(np.mean(results_1,0)[0])
    goodput_case1.append(np.mean(results_1,0)[1])
    AoI_case1.append(np.mean(results_1,0)[3])
    
    "***********************************"
 
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = nNodes, code = '2/3', headers=2, payload_size=n)
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_2 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.

    success_case2.append(np.mean(results_2,0)[0])
    goodput_case2.append(np.mean(results_2,0)[1])
    AoI_case2.append(np.mean(results_2,0)[3])

    "***********************************"
 
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = nNodes, code = '1/2', headers=2, payload_size=n)
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_3 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.

    success_case3.append(np.mean(results_3,0)[0])
    goodput_case3.append(np.mean(results_3,0)[1])
    AoI_case3.append(np.mean(results_3,0)[3])

    "***********************************"
 
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = nNodes, code = '1/3', headers=3, payload_size=n)
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_4 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.

    success_case4.append(np.mean(results_4,0)[0])
    goodput_case4.append(np.mean(results_4,0)[1])
    AoI_case4.append(np.mean(results_4,0)[3])    

    print(n)

print(f"Case 1: Goodput: {goodput_case1} - AoI: {AoI_case1}")
print(f"Case 2: Goodput: {goodput_case2} - AoI: {AoI_case2}")
print(f"Case 3: Goodput: {goodput_case3} - AoI: {AoI_case3}")
print(f"Case 4: Goodput: {goodput_case4} - AoI: {AoI_case4}")


print(f"The simulation lasted {time.perf_counter()-start} seconds.")
