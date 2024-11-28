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

    #####
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
    success_quantity = sum(n.success_quantity for n in nodes)
    transmitted = sum(n.transmitted for n in nodes)


    "Deixei comentado pois estava impedindo o funcionamento do código. (pip install -e .)"
    ###### Soma do total de headers/fragmentos transmitidos por todos os nós da rede.
    total_headers=sum(n.qty_headers for n in nodes)
    total_payloads=sum(n.qty_payloads for n in nodes)
    ######
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
                

    AoI_media = H_i_num/((settings.simulation_time)) 
    
    
    
    

    print(AoI_media) 
    print(success_quantity)
    print(transmitted)
    
    
    if transmitted == 0: 
        return 1
    else:    
        return [[success_quantity/transmitted], [success*settings.payload_size], [transmitted], [total_headers], [total_payloads],[AoI_media]]
        
if __name__ == "__main__":
   s = Settings()
   print(run_sim(s))