"*********Anotações*********"

#Primeira Curva (A):
    #Fixado: 10 de Payload e 1/3 de taxa
    
#Segunda Curva (B):
    #Fixado: 10 de Payload e 3 headers

#Segundo Curva (C):
    #Fixado: 1/3 de taxa e 3 headers

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

"************GRÁFICOS****************"
#'Pontos' de nós (each simulation takes one different)
nNodes_points = 20
#Quantidade mínima de nós
nNodes_min = 1000
#Quantidade mínima de nós
nNodes_max = 150000
#O número de nós é divido por 8, "as we are simulating one of the 8 grid" "<- perguntar."
#Como eles são selecionados aleatoriamente, é uma boa aproximação considerar apenas um deles, e decairá conforme o tempo.
#No final, multiplicamos esse vetor por 8 se quisermos considerar a capacidade total da tecnologia.

nNodes = np.linspace(nNodes_min, nNodes_max, nNodes_points, dtype=int)//8

#Número de loops
loops = 5

start = time.perf_counter()

#Vetores de sucesso ajustado, cada gráfico precisa de 3 vetores success e 3 vetores goodput
success_a1 = []
goodput_a1 = []
success_a2 = []
goodput_a2 = []
success_a3 = []
goodput_a3 = []

success_b1 = []
goodput_b1 = []
success_b2 = []
goodput_b2 = []
success_b3 = []
goodput_b3 = []

success_c1 = []
goodput_c1 = []
success_c2 = []
goodput_c2 = []
success_c3 = []
goodput_c3 = []

#Para cada número de nodes_point, roda a simulação "loops" vezes

for n in nNodes:
    #Variaveis para cada gráfico A:
    s_a1 = Settings(number_nodes = n, headers = 3)
    s_a2 = Settings(number_nodes = n, headers = 4)
    s_a3 = Settings(number_nodes = n, headers = 5)

    #Variaveis para cada gráfico B:    
    s_b1 = Settings(number_nodes = n, code = '1/3')
    s_b2 = Settings(number_nodes = n, code = '2/3')
    s_b3 = Settings(number_nodes = n, code = '5/6')
    
    #Variaveis para cada gráfico C:    
    s_c1 = Settings(number_nodes = n, payload_size = 10)
    s_c2 = Settings(number_nodes = n, payload_size = 30)
    s_c3 = Settings(number_nodes = n, payload_size = 50)
    
    

    #Resultados do gráfico A:
    results_a1 = Parallel(n_jobs=8) (delayed(run_sim)(s_a1, seed = seed) for seed in range(0,loops))
    results_a2 = Parallel(n_jobs=8) (delayed(run_sim)(s_a2, seed = seed) for seed in range(0,loops))
    results_a3 = Parallel(n_jobs=8) (delayed(run_sim)(s_a3, seed = seed) for seed in range(0,loops))
   
    #Resultados do gráfico B:
    results_b1 = Parallel(n_jobs=8) (delayed(run_sim)(s_b1, seed = seed) for seed in range(0,loops))
    results_b2 = Parallel(n_jobs=8) (delayed(run_sim)(s_b2, seed = seed) for seed in range(0,loops))
    results_b3 = Parallel(n_jobs=8) (delayed(run_sim)(s_b3, seed = seed) for seed in range(0,loops))
   
    #Resultados do gráfico C:
    results_c1 = Parallel(n_jobs=8) (delayed(run_sim)(s_c1, seed = seed) for seed in range(0,loops))
    results_c2 = Parallel(n_jobs=8) (delayed(run_sim)(s_c2, seed = seed) for seed in range(0,loops))
    results_c3 = Parallel(n_jobs=8) (delayed(run_sim)(s_c3, seed = seed) for seed in range(0,loops))
    
    #Ajustar sucessos para o gráfico A:
    success_a1.append(np.mean(results_a1,0)[0])
    goodput_a1.append(np.mean(results_a1,0)[2]*np.mean(results_a1,0)[0])
    success_a2.append(np.mean(results_a2,0)[0])
    goodput_a2.append(np.mean(results_a2,0)[2]*np.mean(results_a2,0)[0])
    success_a3.append(np.mean(results_a3,0)[0])
    goodput_a3.append(np.mean(results_a3,0)[2]*np.mean(results_a3,0)[0])
  
    #Ajustar sucessos para o gráfico B:
    success_b1.append(np.mean(results_b1,0)[0])
    goodput_b1.append(np.mean(results_b1,0)[2]*np.mean(results_b1,0)[0])
    success_b2.append(np.mean(results_b2,0)[0])
    goodput_b2.append(np.mean(results_b2,0)[2]*np.mean(results_b2,0)[0])
    success_b3.append(np.mean(results_b3,0)[0])
    goodput_b3.append(np.mean(results_b3,0)[2]*np.mean(results_b3,0)[0])
      
    #Ajustar sucessos para o gráfico C:
    success_c1.append(np.mean(results_c1,0)[0])
    goodput_c1.append(np.mean(results_c1,0)[2]*np.mean(results_c1,0)[0])
    success_c2.append(np.mean(results_c2,0)[0])
    goodput_c2.append(np.mean(results_c2,0)[2]*np.mean(results_c2,0)[0])
    success_c3.append(np.mean(results_c3,0)[0])
    goodput_c3.append(np.mean(results_c3,0)[2]*np.mean(results_c3,0)[0])
      
    print(n*8)
    
print("The simulation lasted {time.perf_counter()-start} seconds.")

#Dataframes
df_a1 = pd.DataFrame({'Success': success_a1, 'Goodput': goodput_a1})
df_a2 = pd.DataFrame({'Success': success_a2, 'Goodput': goodput_a2})
df_a3 = pd.DataFrame({'Success': success_a3, 'Goodput': goodput_a3})

df_b1 = pd.DataFrame({'Success': success_b1, 'Goodput': goodput_b1})
df_b2 = pd.DataFrame({'Success': success_b2, 'Goodput': goodput_b2})
df_b3 = pd.DataFrame({'Success': success_b3, 'Goodput': goodput_b3})


df_c1 = pd.DataFrame({'Success': success_c1, 'Goodput': goodput_c1})
df_c2 = pd.DataFrame({'Success': success_c2, 'Goodput': goodput_c2})
df_c3 = pd.DataFrame({'Success': success_c3, 'Goodput': goodput_c3})

#Abertura de arquivos gráfico A
file = open('grafico_a1.data', 'wb')
pickle.dump(df_a1, file)
file.close()

file = open('grafico_a2.data', 'wb')
pickle.dump(df_a2, file)
file.close()

file = open('grafico_a3.data', 'wb')
pickle.dump(df_a3, file)
file.close()

#Abertura de arquivos gráfico B
file = open('grafico_b1.data', 'wb')
pickle.dump(df_b1, file)
file.close()

file = open('grafico_b2.data', 'wb')
pickle.dump(df_b2, file)
file.close()

file = open('grafico_b3.data', 'wb')
pickle.dump(df_b3, file)
file.close()

#Abertura de arquivos gráfico C
file = open('grafico_c1.data', 'wb')
pickle.dump(df_c1, file)
file.close()

file = open('grafico_c2.data', 'wb')
pickle.dump(df_c2, file)
file.close()

file = open('grafico_c3.data', 'wb')
pickle.dump(df_c3, file)
file.close()


"Plot do gráfico A"   
example_a1 = pd.read_pickle('grafico_a1.data')
example_a2 = pd.read_pickle('grafico_a2.data')
example_a3 = pd.read_pickle('grafico_a3.data')
f_x = EngFormatter()
with plt.style.context(['science', 'ieee', 'no-latex']):
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    pparam = dict(ylabel='Average success delivery ratio',xlabel='Number of nodes')
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(f_x)
    ax.plot(nNodes*8, example_a1['Success'],color='green', label='3 headers')
    ax.plot(nNodes*8, example_a2['Success'],color='blue', label='4 headers')
    ax.plot(nNodes*8, example_a3['Success'],color='red', label='5 headers')
    
    leg = ax.legend(loc=3)

    ax.grid(ls='--', color='lightgray')
    ax.autoscale(tight=True)
    ax.set(**pparam)
    ax.set_ylim(top=1)
    plt.tight_layout()
    plt.show()
    plt.close()   
   
    
"Plot do gráfico B"   
example_b1 = pd.read_pickle('grafico_b1.data')
example_b2 = pd.read_pickle('grafico_b2.data')
example_b3 = pd.read_pickle('grafico_b3.data')
f_x = EngFormatter()
with plt.style.context(['science', 'ieee', 'no-latex']):
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    pparam = dict(ylabel='Average success delivery ratio',xlabel='Number of nodes')
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(f_x)
    ax.plot(nNodes*8, example_b1['Success'],color='green', label='1/3 de CR')
    ax.plot(nNodes*8, example_b2['Success'],color='blue', label='2/3 de CR')
    ax.plot(nNodes*8, example_b3['Success'],color='red', label='5/6 de CR')
    
    leg = ax.legend(loc=3)

    ax.grid(ls='--', color='lightgray')
    ax.autoscale(tight=True)
    ax.set(**pparam)
    ax.set_ylim(top=1)
    plt.tight_layout()
    plt.show()
    plt.close()   

    
"Plot do gráfico C"   
example_c1 = pd.read_pickle('grafico_c1.data')
example_c2 = pd.read_pickle('grafico_c2.data')
example_c3 = pd.read_pickle('grafico_c3.data')
f_x = EngFormatter()
with plt.style.context(['science', 'ieee', 'no-latex']):
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    pparam = dict(ylabel='Average success delivery ratio',xlabel='Number of nodes')
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(f_x)
    ax.plot(nNodes*8, example_c1['Success'],color='green', label='10 P.S.')
    ax.plot(nNodes*8, example_c2['Success'],color='blue', label='30 P.S.')
    ax.plot(nNodes*8, example_c3['Success'],color='red', label='50 P.S.')
    
  
    leg = ax.legend(loc=3)

    ax.grid(ls='--', color='lightgray')
    ax.autoscale(tight=True)
    ax.set(**pparam)
    ax.set_ylim(top=1)
    plt.tight_layout()
    plt.show()
    plt.close()   