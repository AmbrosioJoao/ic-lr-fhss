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
    AoI_media_teste = 0
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
        r_n_1=0
        s_n_1=0
        loop=0
        
        #A variável 'p' recebe o timestamp final associado ao pacote 'n'
        for p in n.final_timestamp:
            
            H_i_num = 0
            H_i_num_teste = 0
            r_n=p
            s_n=n.initial_timestamp[loop]
            ### CALCULA AoI
            H_i=(r_n-r_n_1)*(r_n_1 - s_n_1) + ((r_n - r_n_1)**2)/2
            H_i_num += H_i
             
            ### TESTE 
            H_i_teste = ((r_n + r_n_1 - 2*s_n_1)*(r_n - r_n_1))/2
            H_i_num_teste += H_i_teste
            
            if r_n>0:
                r_n_1=r_n
                s_n_1=s_n
                
            loop=loop+1

    #por algum motivo, ao alterar os valores no settings agora ele altera a média do AoI, o que não aconteceu no dia
    AoI_media_teste = H_i_num_teste/(settings.simulation_time)
    AoI_media = H_i_num/(settings.simulation_time) 
    
    print(AoI_media_teste)
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