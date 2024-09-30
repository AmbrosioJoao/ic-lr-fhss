from lrfhss.lrfhss_core import *
from lrfhss.settings import Settings
import simpy

def run_sim(settings: Settings, seed=0):
    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()
   
    bs = Base(settings.obw, settings.threshold)
    
    nodes = []
    packets = []
    vetor_AoI = []
    AoI_inicial = []
    AoI_final = []
    delta_vector = []
    AoI_media = 0
    
    for i in range(settings.number_nodes):
        node = Node(settings.obw, settings.headers, settings.payloads, settings.header_duration, settings.payload_duration, settings.transceiver_wait, settings.traffic_generator)
        bs.add_node(node.id)
        nodes.append(node)
        env.process(node.transmit(env, bs))
                
    # start simulation
    env.run(until=settings.simulation_time)

    # after simulation
    success = sum(bs.packets_received.values())
    transmitted = sum(n.transmitted for n in nodes)


    "Deixei comentado pois estava impedindo o funcionamento do código. (pip install -e .)"
    ###### Soma do total de headers/fragmentos transmitidos por todos os nós da rede.
    total_headers=sum(n.qty_headers for n in nodes)
    total_payloads=sum(n.qty_payloads for n in nodes)
    ######

    for n in nodes: 
        
    #'Vetor delta'    
        AoI_media += (n.sum_aoi)/(settings.number_nodes) #verificar se é divido por todos os nós ou por 2
               
    print(AoI_media)  
    
     #   print(n.id)
     #   print(AoI_inicial)
     #   print(AoI_final)
        
    if transmitted == 0: 
        return 1
    else:    
        return [[success/transmitted], [success*settings.payload_size], [transmitted], [total_headers], [total_payloads]]
        
        

if __name__ == "__main__":
   s = Settings()
   print(run_sim(s))