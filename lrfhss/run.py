from lrfhss.lrfhss_core import *
from lrfhss.acrda import BaseACRDA
from lrfhss.settings import Settings
import simpy

def run_sim(settings: Settings, seed=0):
    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()
    bs = Base(settings.obw, settings.threshold)
    
    nodes = []
    
    for i in range(settings.number_nodes):
        node = Node(settings.obw, settings.headers, settings.payloads, settings.header_duration, settings.payload_duration, settings.transceiver_wait, settings.traffic_generator)
        bs.add_node(node.id)
        nodes.append(node)
        env.process(node.transmit(env, bs))
    # start simulation
    env.run(until=settings.simulation_time)

    # after simulation

    ######## Cálculo da AoI ########  
    H_i_num = 0
    
    for n in nodes: 
      r_n_1=0
      s_n_1=0
      loop=0
      
      #H_i_num = 0
      
      #A variável 'p' recebe o timestamp final associado ao pacote 'n'
      for p in n.final_timestamp:
          
         # H_i_num = 0
          if(n.final_timestamp != 0 ):   
              r_n=p
              s_n=n.initial_timestamp[loop]
          ### CALCULA AoI
              H_i=(r_n-r_n_1)*(r_n_1 - s_n_1) + ((r_n - r_n_1)**2)/2
              H_i_num += H_i

          if(n.final_timestamp == 0 ):  
              
                  H_i = 0
                  H_i_num += H_i 
          
          if r_n>0:
                  r_n_1=r_n
                  s_n_1=s_n
              
          loop=loop+1

    AoI_media = (H_i_num/((settings.simulation_time))/settings.number_nodes) 
    
    ######## Cálculo da AoI ######## 

    success = sum(bs.packets_received.values())
    transmitted = sum(n.transmitted for n in nodes)

    if transmitted == 0: #If no transmissions are made, we consider 100% success as there were no outages
        return 1
    else:
        
        #sucess rate, goodput , transmitidos, aoi media
        return [[success/transmitted], [success*settings.payload_size], [transmitted], [AoI_media]]

    #Get the average success per device, used to plot the CDF 
    #success_per_device = [1 if n.transmitted == 0 else bs.packets_received[n.id]/n.transmitted for n in nodes]
    #return success_per_device
if __name__ == "__main__":
   s = Settings()
   print(run_sim(s))