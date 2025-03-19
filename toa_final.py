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
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

"***********TOA***************"
def toa(settings: Settings, seed=0):
    
    #Variáveis que mudam conforme a classe settings.py
    headers_time = settings.headers
    payloads_time = settings.payloads
    toa = (headers_time*settings.header_duration + payloads_time*settings.payload_duration)
    
    
    return toa

settings_config = Settings()  

toa_sim = toa(settings_config)

print(toa_sim)
"*****************************" 

#'Pontos' de nós (each simulation takes one different)
nNodes_points = 20
#Quantidade mínima de nós
nNodes_min = 1000
#Quantidade mínima de nós
nNodes_max = 150000
#O número de nós é divido por 8.
#Como eles são selecionados aleatoriamente, é uma boa aproximação considerar apenas um deles, e decairá conforme o tempo.
#No final, multiplicamos esse vetor por 8 se quisermos considerar a capacidade total da tecnologia.

nNodes = np.linspace(nNodes_min, nNodes_max, nNodes_points, dtype=int)//8

#Número de loops
loops = 5
start = time.perf_counter()

courses = list(nNodes)
values = list(nNodes)

valores_toa = [value * toa_sim for value in values]
plt.gca().xaxis.set_major_formatter(EngFormatter(unit='', places=0))
plt.gca().yaxis.set_major_formatter(EngFormatter(unit='', places=0))
plt.bar(courses, valores_toa , color ='green', width = 700)

plt.xlabel("Dispositivos")
plt.ylabel("ToA")




plt.show()