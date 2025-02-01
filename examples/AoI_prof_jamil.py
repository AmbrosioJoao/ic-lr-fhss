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
"***************************"


#Number of different number of nodes points (each simulation takes one different)
nNodes_points = 5
#Mininum amount of nodes
nNodes_min = 1000
#Maximum amount of nodes
nNodes_max = 15000
#Number of nodes is divided by 8, as we are simulating one of the 8 grid.
#As they are random selected, it is a very good approximation to consider one of them only, and it decreases the simulation time.
#In the end, we multiply this array by 8 if we want to consider the technology total capacity.
nNodes = np.linspace(nNodes_min, nNodes_max, nNodes_points, dtype=int)//8
#Number of simulation loops for each configuration.
loops = 1

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
for n in nNodes:
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = n, code = '1/3')
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_1 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.
    success_case1.append(np.mean(results_1,0)[0])
    goodput_case1.append(np.mean(results_1,0)[2]*np.mean(results_1,0)[0])
    AoI_case1.append(np.mean(results_1,0)[3])
    
    "***********************************"
 
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = n, code = '1/2')
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_2 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.

    success_case2.append(np.mean(results_2,0)[0])
    goodput_case2.append(np.mean(results_2,0)[2]*np.mean(results_2,0)[0])
    AoI_case2.append(np.mean(results_2,0)[3])

    "***********************************"
 
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = n, code = '2/3')
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_3 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.

    success_case3.append(np.mean(results_3,0)[0])
    goodput_case3.append(np.mean(results_3,0)[2]*np.mean(results_3,0)[0])
    AoI_case3.append(np.mean(results_3,0)[3])

    "***********************************"
 
    #For each nNodes, create a new settings object with the proper input parameter
    s = Settings(number_nodes = n, code = '5/6')
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_4 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.

    success_case4.append(np.mean(results_4,0)[0])
    goodput_case4.append(np.mean(results_4,0)[2]*np.mean(results_4,0)[0])
    AoI_case4.append(np.mean(results_4,0)[3])    





    print(n*8)


print(f"Case 1: Goodput: {goodput_case1} - AoI: {AoI_case1}")
print(f"Case 2: Goodput: {goodput_case2} - AoI: {AoI_case2}")
print(f"Case 3: Goodput: {goodput_case3} - AoI: {AoI_case3}")
print(f"Case 4: Goodput: {goodput_case4} - AoI: {AoI_case4}")


print(f"The simulation lasted {time.perf_counter()-start} seconds.")

#Saving results on a file
df_1 = pd.DataFrame({'Average AoI': AoI_case1}, index = nNodes)
file = open('example_case1.data', 'wb')
pickle.dump(df_1, file)
file.close()

#Saving results on a file
df_2 = pd.DataFrame({'Average AoI': AoI_case2}, index = nNodes)
file = open('example_case2.data', 'wb')
pickle.dump(df_2, file)
file.close()

#Saving results on a file
df_3 = pd.DataFrame({'Average AoI': AoI_case3}, index = nNodes)
file = open('example_case3.data', 'wb')
pickle.dump(df_3, file)
file.close()

#Saving results on a file
df_4 = pd.DataFrame({'Average AoI': AoI_case4}, index = nNodes)
file = open('example_case4.data', 'wb')
pickle.dump(df_4, file)
file.close()


"Plot do gráfico 1"   
example_1 = pd.read_pickle('example_case1.data')
example_2 = pd.read_pickle('example_case2.data')
example_3 = pd.read_pickle('example_case3.data')
example_4 = pd.read_pickle('example_case4.data')


#IMPORTANTE, como são listas, pesquisei como obter somente o último resultado dos appends realizados
aoi_int_1 = example_1['Average AoI'].tolist()[-1]
aoi_int_2 = example_2['Average AoI'].tolist()[-1] 
aoi_int_3 = example_3['Average AoI'].tolist()[-1]
aoi_int_4 = example_4['Average AoI'].tolist()[-1]



f_x = EngFormatter()


with plt.style.context(['science', 'ieee', 'no-latex']):
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    pparam = dict(ylabel='Average AoI', xlabel='Number of nodes')
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(f_x)
    
    ax.plot(nNodes/1000000, (nNodes* aoi_int_1)/1000000 , color='green', label='1/3 C.R.')
    ax.plot(nNodes/1000000, (nNodes*aoi_int_2)/1000000 , color='blue', label='1/2 C.R.')
    ax.plot(nNodes/1000000, (nNodes*aoi_int_3)/1000000 , color='red', label='2/3 C.R.')
    ax.plot(nNodes/1000000, (nNodes*aoi_int_4)/1000000 , color='magenta', label='5/6 C.R.')    
    
    leg = ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.8, edgecolor='black')
    ax.grid(ls='--', color='lightgray')
    ax.autoscale(tight=True)
    ax.set(**pparam)
    ax.set_ylim(bottom=0)  # Ajuste conforme necessário
    plt.tight_layout()
    plt.show()
    plt.close()


