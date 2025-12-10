from lrfhss.run import *
import time
from joblib import Parallel, delayed
import numpy as np
import scipy as sp
import pickle
import pandas as pd

# Número de pontos de simulação
nNodes_points = 20
# Mínimo de nós
nNodes_min = 1000
# Máximo de nós
nNodes_max = 150000

# Divisão por 8 conforme a grid espacial
nNodes = np.linspace(nNodes_min, nNodes_max, nNodes_points, dtype=int)//8
# Loops de simulação
loops = 10

# Tempo de simulação (Necessário para converter Total Pacotes -> Taxa Pacotes/s)
# Baseado na sua normalização do MATLAB
sim_duration = 3600.0 

start = time.perf_counter()

goodput_case1 = []
efficiency_1 = []

goodput_case2 = []
efficiency_2 = []

goodput_case3 = []
efficiency_3 = []

goodput_case4 = []
efficiency_4 = []

# Loop principal
for n in nNodes:
    
    # =========================================================
    # CUSTOM - 1 (CR: 5/6, Headers: 1)
    # =========================================================
    s = Settings(number_nodes = n, code = '5/6', headers=1, tx_power=0.01, delta = 1, traffic_param = {'average_interval': 900}, header_duration = 0.233472, payload_duration = 0.100)
    
    results_1 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    
    code_number_1 = 5/6
    
    # Pega a média do total de pacotes (índice 1 do resultado)
    current_goodput_total = np.mean(results_1, 0)[1]
    goodput_case1.append(current_goodput_total)
    
    headers_average_1 = s.headers
    threshold_average_1 = int(np.ceil((s.payload_size + 3) / (6 * code_number_1)))
    traffic_param_1 = 900
    
    # CÁLCULO CORRIGIDO:
    # 1. Numerador: Taxa (Pacotes/seg) = Total / Tempo
    goodput_rate = current_goodput_total / sim_duration
    
    # 2. Denominador: Potência Média (Watts)
    avg_power = s.tx_power * ((n*(1/traffic_param_1)) * (headers_average_1*s.header_duration + threshold_average_1*s.payload_duration))
    
    # 3. Append apenas do valor atual (sem média da lista histórica)
    efficiency_1.append(goodput_rate / avg_power)

    
    # =========================================================
    # DR9 (CR: 2/3, Headers: 2)
    # =========================================================
    s = Settings(number_nodes = n, code = '2/3', headers=2, tx_power=0.01, delta = 1, traffic_param = {'average_interval': 900}, header_duration = 0.233472, payload_duration = 0.100)
    
    results_2 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    
    code_number_2 = 2/3
    
    current_goodput_total = np.mean(results_2, 0)[1]
    goodput_case2.append(current_goodput_total)
    
    threshold_average_2 = int(np.ceil((s.payload_size + 3) / (6 * code_number_2)))
    headers_average_2 = s.headers
    traffic_param_2 = 900
    
    goodput_rate = current_goodput_total / sim_duration
    avg_power = s.tx_power * ((n*(1/traffic_param_2)) * (headers_average_2*s.header_duration + threshold_average_2*s.payload_duration))
    
    efficiency_2.append(goodput_rate / avg_power)
    
    
    # =========================================================
    # CUSTOM 2 (CR: 1/2, Headers: 2)
    # =========================================================
    s = Settings(number_nodes = n, code = '1/2', headers=2, tx_power=0.01, delta = 1, traffic_param = {'average_interval': 900}, header_duration = 0.233472, payload_duration = 0.100)
    
    results_3 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    
    code_number_3 = 1/2
    
    current_goodput_total = np.mean(results_3, 0)[1]
    goodput_case3.append(current_goodput_total)
    
    headers_average_3 = s.headers
    threshold_average_3 = int(np.ceil((s.payload_size + 3) / (6 * code_number_3)))
    traffic_param_3 = 900
    
    goodput_rate = current_goodput_total / sim_duration
    avg_power = s.tx_power * ((n*(1/traffic_param_3)) * (headers_average_3*s.header_duration + threshold_average_3*s.payload_duration))
    
    efficiency_3.append(goodput_rate / avg_power)

    
    # =========================================================
    # DR8 (CR: 1/3, Headers: 3)
    # =========================================================
    s = Settings(number_nodes = n, code = '1/3', headers=3, tx_power=0.01, delta = 1, traffic_param = {'average_interval': 900}, header_duration = 0.233472, payload_duration = 0.100)
    
    results_4 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    
    code_number_4 = 1/3
    
    current_goodput_total = np.mean(results_4, 0)[1]
    goodput_case4.append(current_goodput_total)
    
    headers_average_4 = s.headers
    threshold_average_4 = int(np.ceil((s.payload_size + 3) / (6 * code_number_4)))
    traffic_param_4 = 900
    
    goodput_rate = current_goodput_total / sim_duration
    avg_power = s.tx_power * ((n*(1/traffic_param_4)) * (headers_average_4*s.header_duration + threshold_average_4*s.payload_duration))
    
    efficiency_4.append(goodput_rate / avg_power)

    
    # Print de controle
    print(n*8)

print(f"The simulation lasted {time.perf_counter()-start} seconds.")