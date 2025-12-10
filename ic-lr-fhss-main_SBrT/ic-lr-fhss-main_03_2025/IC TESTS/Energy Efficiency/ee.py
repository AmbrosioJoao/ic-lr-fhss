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


#Number of different number of nodes points (each simulation takes one different)
nNodes_points = 20
#Mininum amount of nodes
nNodes_min = 1000
#Maximum amount of nodes
nNodes_max = 150000
#Number of nodes is divided by 8, as we are simulating one of the 8 grid.
#As they are random selected, it is a very good approximation to consider one of them only, and it decreases the simulation time.
#In the end, we multiply this array by 8 if we want to consider the technology total capacity.
nNodes = np.linspace(nNodes_min, nNodes_max, nNodes_points, dtype=int)//8
#Number of simulation loops for each configuration.
loops = 10

start = time.perf_counter()

goodput_case1 = []
efficiency_1 = []

goodput_case2 = []
efficiency_2 = []

goodput_case3 = []
efficiency_3 = []

goodput_case4 = []
efficiency_4 = []

#For each number of nodes point, run the simulation "loops" times
for n in nNodes:
    #For each nNodes, create a new settings object with the proper input parameter
    
    #CUSTOM - 1
    s = Settings(number_nodes = n, code = '5/6', headers=1, tx_power=0.01, delta = 1, traffic_param = {'average_interval': 900}, header_duration = 0.233472, payload_duration = 0.100)
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_1 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    
    code_number_1 = 5/6
   
    # CONVERT THE LIST TO A NUMPY ARRAY BEFORE INDEXING
#    results_1 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.
    goodput_case1.append(np.mean(results_1,0)[1])
 
    #threshold_1 = np.ceil(s.payload_size+3/(6*code_number_1)).astype('int')

    headers_average_1 = s.headers
    #threshold_average_1 = s.payloads
    threshold_average_1 = int( np.ceil( (s.payload_size + 3) / (6 * code_number_1) ) )
    traffic_param_1 = 900
    
    #s.tx_power -- converter para Watt. ( 10dBm -> 0,01 W)
    
    efficiency_1.append(np.mean(goodput_case1/(s.tx_power*((n*(1/traffic_param_1))*(headers_average_1*s.header_duration+threshold_average_1*s.payload_duration)))))
    "***********************************"
 
    #DR9
    s = Settings(number_nodes = n, code = '2/3', headers=2, tx_power=0.01, delta = 1, traffic_param = {'average_interval': 900}, header_duration = 0.233472, payload_duration = 0.100)
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_2 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    
    code_number_2 = 2/3
   
    # CONVERT THE LIST TO A NUMPY ARRAY BEFORE INDEXING
 #   results_2 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.
    goodput_case2.append(np.mean(results_2,0)[1])
 
    #threshold_2 = np.ceil(s.payload_size+3/(6*code_number_2)).astype('int')
    
   #threshold_average_2 = s.payloads
    threshold_average_2 = int( np.ceil( (s.payload_size + 3) / (6 * code_number_2) ) )
    headers_average_2 = s.headers

    traffic_param_2 = 900
    
    efficiency_2.append(np.mean(goodput_case2/(s.tx_power*((n*(1/traffic_param_2))*(headers_average_2*s.header_duration+threshold_average_2*s.payload_duration)))))
    
    "***********************************"
  
    #CUSTOM 2
    s = Settings(number_nodes = n, code = '1/2', headers=2, tx_power=0.01, delta = 1, traffic_param = {'average_interval': 900}, header_duration = 0.233472, payload_duration = 0.100)
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_3 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    
    code_number_3 = 1/2
   
    # CONVERT THE LIST TO A NUMPY ARRAY BEFORE INDEXING
 #   results_3 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
    
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.
    goodput_case3.append(np.mean(results_3,0)[1])
 
    #threshold_3 = np.ceil(s.payload_size+3/(6*code_number_3)).astype('int')

    headers_average_3 = s.headers
   # threshold_average_3 = s.payloads
    threshold_average_3 = int( np.ceil( (s.payload_size + 3) / (6 * code_number_3) ) )
    traffic_param_3 = 900
   
    
    efficiency_3.append(np.mean(goodput_case3/(s.tx_power*((n*(1/traffic_param_3))*(headers_average_3*s.header_duration+threshold_average_3*s.payload_duration)))))

    "***********************************"

    #DR8
    s = Settings(number_nodes = n, code = '1/3', headers=3, tx_power=0.01, delta = 1, traffic_param = {'average_interval': 900}, header_duration = 0.233472, payload_duration = 0.100)
    #This line runs the simulation loops in paralel, using n_jobs as the number of threads generated.
    #Consider using a number according to the amount of reseources available to your machine to avoid crashing your system.
    results_4 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
   
    code_number_4 = 1/3
  
    # CONVERT THE LIST TO A NUMPY ARRAY BEFORE INDEXING
 #   results_4 = Parallel(n_jobs=8) (delayed(run_sim)(s, seed = seed) for seed in range(0,loops))
   
    #At the moment we only get the network outage probability as results and append the mean of the loops (for better accuracy) to a list.
    goodput_case4.append(np.mean(results_4,0)[1])

  #  threshold_4 = np.ceil(s.payload_size+3/(6*code_number_4)).astype('int')

    headers_average_4 = s.headers
    #threshold_average_4 = s.payloads
    threshold_average_4 = int( np.ceil( (s.payload_size + 3) / (6 * code_number_4) ) )
    traffic_param_4 = 900

    
    efficiency_4.append(np.mean(goodput_case4/(s.tx_power*((n*(1/traffic_param_4))*(headers_average_4*s.header_duration+threshold_average_4*s.payload_duration)))))

   
    print(n*8)


    


print(f"The simulation lasted {time.perf_counter()-start} seconds.")
