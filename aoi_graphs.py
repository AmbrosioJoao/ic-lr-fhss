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
    #Fixado: 5/6 de taxa
    
#Segunda Curva (B):
    #Fixado: 2/3 de taxa

#Terceira Curva (C):
    #Fixado: 1/2 de taxa
    
#Quarta Curva (D):
    #Fixado: 1/3 de taxa 
    

"***************************"



"***********AoI*************"



#'Pontos' de nós (each simulation takes one different)
#nNodes_points = 20
#Quantidade mínima de nós
#nNodes_min = 1000
#Quantidade mínima de nós
#nNodes_max = 150000
#O número de nós é divido por 8, "as we are simulating one of the 8 grid" "<- perguntar."
#Como eles são selecionados aleatoriamente, é uma boa aproximação considerar apenas um deles, e decairá conforme o tempo.
#No final, multiplicamos esse vetor por 8 se quisermos considerar a capacidade total da tecnologia.
#
#nNodes = np.linspace(nNodes_min, nNodes_max, nNodes_points, dtype=int)//8


nHeaders_points = 20

nHeaders_min = 1 

nHeaders_max = 30

nHeaders = np.linspace(nHeaders_min, nHeaders_max, nHeaders_points, dtype=int)



#Número de loops
loops = 5

start = time.perf_counter()

#Vetores de sucesso ajustado, cada gráfico precisa de 3 vetores success e 3 vetores goodput
success_a1, goodput_a1, aoI_media_a1 = [], [], []
success_b1, goodput_b1, aoI_media_b1 = [], [], []
success_c1, goodput_c1, aoI_media_c1 = [], [], []

#Para cada número de nodes_point, roda a simulação "loops" vezes

for n in nHeaders:
    #Variaveis para cada gráfico 1:
    s_a1 = Settings(headers = n , code = '5/6' )
 #   s_b1 = Settings(headers = n , code = '2/3')
 #   s_c1 = Settings(headers = n , code = '1/3')

  # Resultados do gráfico A:
    results_a1 = Parallel(n_jobs=8)(delayed(run_sim)(s_a1, seed=seed) for seed in range(loops))
 #  results_b1 = Parallel(n_jobs=8)(delayed(run_sim)(s_b1, seed=seed) for seed in range(loops))
  # results_c1 = Parallel(n_jobs=8)(delayed(run_sim)(s_c1, seed=seed) for seed in range(loops))

    # Ajustar sucessos e AoI_media para o gráfico A:
   
    success_a1.append(np.mean(results_a1, 0)[5])
   
   # goodput_a1.append(np.mean(results_a1, 0)[2] * np.mean(results_a1, 0)[5])
    aoI_media_a1.append(np.mean(results_a1, 0)[5])  # Índice 5 para AoI_media

   # teste = (np.mean(results_a1, 0)[5])
 #   success_b1.append(np.mean(results_b1, 0)[0])
  #  goodput_b1.append(np.mean(results_b1, 0)[5] * np.mean(results_b1, 0)[0])
 #   aoI_media_b1.append(np.mean(results_b1, 0)[5])  # Índice 5 para AoI_media

 #   success_c1.append(np.mean(results_c1, 0)[0])
 #   goodput_c1.append(np.mean(results_c1, 0)[5] * np.mean(results_c1, 0)[0])
 #   aoI_media_c1.append(np.mean(results_c1, 0)[5])  # Índice 5 para AoI_media
  
    print(n)
    
print("The simulation lasted {time.perf_counter()-start} seconds.")

#Dataframes
#df_a1 = pd.DataFrame({'Success': success_a1, 'Goodput': goodput_a1, 'AoI Media': aoI_media_a1})
df_a1 = pd.DataFrame({'Success': success_a1, 'AoI Media': aoI_media_a1})
#df_b1 = pd.DataFrame({'Success': success_b1, 'Goodput': goodput_b1, 'AoI Media': aoI_media_b1})
#df_c1 = pd.DataFrame({'Success': success_c1, 'Goodput': goodput_c1, 'AoI Media': aoI_media_c1})


#Abertura de arquivos gráfico A
file = open('Curva_A1.data', 'wb')
pickle.dump(df_a1, file)
file.close()

#file = open('Curva_B1.data', 'wb')
#pickle.dump(df_b1, file)
#file.close()

#file = open('Curva_C1.data', 'wb')
##pickle.dump(df_c1, file)
#file.close()


"Plot do gráfico 1"   
example_a1 = pd.read_pickle('Curva_A1.data')
#example_b1 = pd.read_pickle('Curva_B1.data')
#example_c1 = pd.read_pickle('Curva_C1.data')
aoi_media_teste = example_a1['AoI Media']
product = nHeaders * aoi_media_teste
f_x = EngFormatter()


with plt.style.context(['science', 'ieee', 'no-latex']):
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    pparam = dict(ylabel='Average AoI Media', xlabel='Number of nodes')
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(f_x)

    # Mudança para o eixo x virar headers
    ax.plot(nHeaders, product , color='green', label='3 headers')
 #   ax.plot(nHeaders, aoI_media_b1, color='blue', label='4 headers')
 #   ax.plot(nHeaders, aoI_media_c1, color='red', label='5 headers')

    # Limitar o eixo x
    ax.set_xlim(left=0, right=7)  # Ajuste os valores conforme necessário

    
    
    
    leg = ax.legend(loc=3)
    ax.grid(ls='--', color='lightgray')
    ax.autoscale(tight=True)
    ax.set(**pparam)
    ax.set_ylim(bottom=0)  # Ajuste conforme necessário
    plt.tight_layout()
    plt.show()
    plt.close()
    
 