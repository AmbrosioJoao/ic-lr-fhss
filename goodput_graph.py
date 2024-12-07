"****************************"

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
import matplotlib.pyplot as plt 


"*********Anotações*********"

#Primeira Curva (A):
    #Fixado: 1/3 de taxa
    
#Segunda Curva (B):
    #Fixado: 2/3 de taxa

#Terceira Curva (C):
    #Fixado: 1/2 de taxa
    
#Quarta Curva (D):
    #Fixado: 5/6 de taxa 
    

"***************************"



"***********AoI*************"


#Alterado pois os headers são valores inteiros
nHeaders_points = 7

nHeaders_min = 1 

nHeaders_max = 7

nNodes = np.linspace(nHeaders_min, nHeaders_max, nHeaders_points, dtype=int)

#Número de loops
loops = 5

start = time.perf_counter()

#Vetores de sucesso ajustado, cada gráfico precisa de 3 vetores success e 3 vetores goodput
success_ga1, goodput_a1 = [], []
success_gb1, goodput_b1 = [], []
success_gc1, goodput_c1 = [], []
success_gd1, goodput_d1 = [], []




#Para cada número de nodes_point, roda a simulação "loops" vezes

for n in nNodes:
    
    s_ga1 = Settings(headers = n , code = '1/3' )
    s_gb1 = Settings(headers = n , code = '2/3' )
    s_gc1 = Settings(headers = n , code = '1/2' )
    s_gd1 = Settings(headers = n , code = '5/6' )

  # Resultados do gráfico A:
    "IMPORTANTE: return [[success/transmitted], [success*settings.payload_size], [transmitted], [total_headers], [total_payloads],[AoI_media]]"    
    results_ga1 = Parallel(n_jobs=8)(delayed(run_sim)(s_ga1, seed=seed) for seed in range(loops))
    results_gb1 = Parallel(n_jobs=8)(delayed(run_sim)(s_gb1, seed=seed) for seed in range(loops))
    results_gc1 = Parallel(n_jobs=8)(delayed(run_sim)(s_gc1, seed=seed) for seed in range(loops))
    results_gd1 = Parallel(n_jobs=8)(delayed(run_sim)(s_gd1, seed=seed) for seed in range(loops))
        
    
    

    goodput_a1 = np.mean(results_ga1, 0)[0] # Índice 5 para AoI_media
    goodput_b1 = np.mean(results_gb1, 0)[0] # Índice 5 para AoI_media
    goodput_c1 = np.mean(results_gc1, 0)[0] # Índice 5 para AoI_media
    goodput_d1 = np.mean(results_gd1, 0)[0] # Índice 5 para AoI_media


  
    

#print("The simulation lasted {time.perf_counter()-start} seconds.")

#Dataframes

dfg_a1 = pd.DataFrame({'GOODPUT': goodput_a1})
dfg_b1 = pd.DataFrame({'GOODPUT': goodput_b1})
dfg_c1 = pd.DataFrame({'GOODPUT': goodput_c1})
dfg_d1 = pd.DataFrame({'GOODPUT': goodput_d1})

#Abertura de arquivos gráfico 1
file = open('Goodput_A1.data', 'wb')
pickle.dump(dfg_a1, file)
file.close()

file = open('Goodput_B1.data', 'wb')
pickle.dump(dfg_b1, file)
file.close()

file = open('Goodput_C1.data', 'wb')
pickle.dump(dfg_c1, file)
file.close()

file = open('Goodput_D1.data', 'wb')
pickle.dump(dfg_d1, file)
file.close()




f_x = EngFormatter()


with plt.style.context(['science', 'ieee', 'no-latex']):
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    pparam = dict(ylabel='Average Goodput', xlabel='Number of headers')
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(f_x)
    
    # Limitar o eixo y
    ax.set_ylim(0, 1)

    ax.plot(nNodes, nNodes*goodput_a1 , color='green', label='1/3 C.R.')
    ax.plot(nNodes, nNodes*goodput_b1 , color='blue', label='2/3 C.R.')
    ax.plot(nNodes, nNodes*goodput_c1 , color='red', label='1/2 C.R.')
    ax.plot(nNodes, nNodes*goodput_d1 , color='magenta', label='5/6 C.R.')    
    
    leg = ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.8, edgecolor='black')
    ax.grid(ls='--', color='lightgray')
    ax.autoscale(tight=True)
    ax.set(**pparam)
    ax.set_ylim(bottom=0)  # Ajuste conforme necessário
    plt.tight_layout()
    plt.show()
    plt.close()
    
 