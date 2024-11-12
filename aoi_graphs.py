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
success_a1, aoI_media_a1 = [], []
success_b1, aoI_media_b1 = [], []
success_c1, aoI_media_c1 = [], []
success_d1, aoI_media_d1 = [], []

#Para cada número de nodes_point, roda a simulação "loops" vezes

for n in nNodes:
    
    s_a1 = Settings(headers = n , code = '1/3' )
    s_b1 = Settings(headers = n , code = '2/3' )
    s_c1 = Settings(headers = n , code = '1/2' )
    s_d1 = Settings(headers = n , code = '5/6' )

  # Resultados do gráfico A:
    results_a1 = Parallel(n_jobs=8)(delayed(run_sim)(s_a1, seed=seed) for seed in range(loops))
    results_b1 = Parallel(n_jobs=8)(delayed(run_sim)(s_b1, seed=seed) for seed in range(loops))
    results_c1 = Parallel(n_jobs=8)(delayed(run_sim)(s_c1, seed=seed) for seed in range(loops))
    results_d1 = Parallel(n_jobs=8)(delayed(run_sim)(s_d1, seed=seed) for seed in range(loops))


    aoI_media_a1 = np.mean(results_a1, 0)[5] # Índice 5 para AoI_media
    aoI_media_b1 = np.mean(results_b1, 0)[5] # Índice 5 para AoI_media
    aoI_media_c1 = np.mean(results_c1, 0)[5] # Índice 5 para AoI_media
    aoI_media_d1 = np.mean(results_d1, 0)[5] # Índice 5 para AoI_media


#print("The simulation lasted {time.perf_counter()-start} seconds.")

#Dataframes

df_a1 = pd.DataFrame({'AoI Media': aoI_media_a1})
df_b1 = pd.DataFrame({'AoI Media': aoI_media_b1})
df_c1 = pd.DataFrame({'AoI Media': aoI_media_c1})
df_d1 = pd.DataFrame({'AoI Media': aoI_media_d1})

#Abertura de arquivos gráfico A
file = open('Curva_A1.data', 'wb')
pickle.dump(df_a1, file)
file.close()

file = open('Curva_B1.data', 'wb')
pickle.dump(df_b1, file)
file.close()

file = open('Curva_C1.data', 'wb')
pickle.dump(df_c1, file)
file.close()

file = open('Curva_D1.data', 'wb')
pickle.dump(df_d1, file)
file.close()


"Plot do gráfico 1"   
example_a1 = pd.read_pickle('Curva_A1.data')
example_b1 = pd.read_pickle('Curva_B1.data')
example_c1 = pd.read_pickle('Curva_C1.data')
example_d1 = pd.read_pickle('Curva_D1.data')


#IMPORTANTE, Ao captar o valor 5 do vetor que o run.py retorna, ele dá um vetor de UMA posição, e o python não admite essa multiplicação de vetores, portanto vou transformar o ultimo valor em int.
aoi_int_a1 = int(example_a1['AoI Media'])
aoi_int_b1 = int(example_b1['AoI Media'])
aoi_int_c1 = int(example_c1['AoI Media'])
aoi_int_d1 = int(example_d1['AoI Media'])


f_x = EngFormatter()


with plt.style.context(['science', 'ieee', 'no-latex']):
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    pparam = dict(ylabel='Average AoI Media', xlabel='Number of headers')
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(f_x)
    
    # Limitar o eixo y
    ax.set_ylim(0, 700)

    ax.plot(nNodes, nNodes*aoi_int_a1 , color='green', label='1/3 C.R.')
    ax.plot(nNodes, nNodes*aoi_int_b1 , color='blue', label='2/3 C.R.')
    ax.plot(nNodes, nNodes*aoi_int_c1 , color='red', label='1/2 C.R.')
    ax.plot(nNodes, nNodes*aoi_int_d1 , color='magenta', label='5/6 C.R.')    
    
    leg = ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.8, edgecolor='black')
    ax.grid(ls='--', color='lightgray')
    ax.autoscale(tight=True)
    ax.set(**pparam)
    ax.set_ylim(bottom=0)  # Ajuste conforme necessário
    plt.tight_layout()
    plt.show()
    plt.close()
    
 