import random
import numpy as np
from abc import ABC, abstractmethod

"Simplest class of the program, containing information about the packets."     
class Fragment():
    def __init__(self, type, duration, channel, packet):
        self.packet = packet 
        self.duration = duration 
        self.success = 0 
        self.transmitted = 0 
        self.type = type 
        self.channel = channel 
        self.timestamp = 0 
        self.id = id(self) 
        self.collided = [] 

"Generates a package structure using the 'Fragment' class."
class Packet():
    #
    def __init__(self, node_id, obw, headers, payloads, header_duration, payload_duration):
        self.id = id(self) 
        self.node_id = node_id
        self.index_transmission = 0
        self.success = 0
        self.channels = random.choices(range(obw), k=headers+payloads)
        self.fragments = []
        
        ######
        #Variables for the calculation of AoI
        self.AoI_inicial= 0
        self.AoI_final = 0
        ######
        
        for h in range(headers):
            self.fragments.append(Fragment('header',header_duration, self.channels[h], self.id))
        for p in range(payloads):
            self.fragments.append(Fragment('payload',payload_duration, self.channels[p+h+1], self.id))

    def next(self):
        self.index_transmission+=1
        try:
            return self.fragments[self.index_transmission-1]
        except:
            return False


"The 'abstract' class used by the Node is responsible for returning the transmission interval between packets"
class Traffic(ABC):
    @abstractmethod
    def __init__(self, traffic_param):
        self.traffic_param = traffic_param

    @abstractmethod
    def traffic_function(self):
        pass


"Represents the 'end-devices'; Here there is a 'transmission routine' that will be executed throughout the entire simulation for each device"
"Generates a new packet to be transported using a 'traffic pattern' -> traffic class; it has the information on how many packets have been transmitted"
class Node():
    def __init__(self, obw, headers, payloads, header_duration, payload_duration, transceiver_wait, traffic_generator):
        self.id = id(self)
        self.transmitted = 0
        self.traffic_generator = traffic_generator
        self.transceiver_wait = transceiver_wait
        self.obw = obw
        self.headers = headers
        self.payloads = payloads
        self.header_duration = header_duration
        self.payload_duration = payload_duration
        self.success_quantity = 0
        ######
        #Arrays that store when the packets were generated and when they finish being received
        self.initial_timestamp = []
        self.final_timestamp = []
        ######
        
        self.qty_headers=0
        self.qty_payloads=0
        self.packet = Packet(self.id, self.obw, self.headers, self.payloads, self.header_duration, self.payload_duration)
   
   
    def next_transmission(self):
        return self.traffic_generator.traffic_function()
        
    def end_of_transmission(self):
        self.packet = Packet(self.id, self.obw, self.headers, self.payloads, self.header_duration, self.payload_duration)
        
       

    def transmit(self, env, bs):
        while 1:
            
            yield env.timeout(self.next_transmission())
            self.transmitted += 1
            bs.add_packet(self.packet)
            next_fragment = self.packet.next()

            ###### When transmitting a packet, include in the variables below the number of headers and fragments transmitted
            self.qty_headers += self.headers
            self.qty_payloads += self.payloads
            ###### 
            
            ###### Initial AoI
            
            ##Verificador 1
          # if bs.try_decode(self.packet,env.now) == True:
            self.packet.AoI_inicial=env.now
            self.initial_timestamp.append(self.packet.AoI_inicial)
                
            ##Verificador 2
         #  if bs.try_decode(self.packet,env.now) == False:
             
            # self.packet.AoI_inicial=0
            # self.initial_timestamp.append(self.packet.AoI_inicial)
                
            
            ###### 
            
            first_payload = 0
            while next_fragment:
                
                if first_payload == 0 and next_fragment.type=='payload': 
                    first_payload=1
                    yield env.timeout(self.transceiver_wait)
                next_fragment.timestamp = env.now

                bs.check_collision(next_fragment)
              
                bs.receive_packet(next_fragment)
     
                yield env.timeout(next_fragment.duration)
       
                bs.finish_fragment(next_fragment)
 
                 
                 
                if self.packet.success == 0:
                    bs.try_decode(self.packet,env.now)
                    
                   
                    
                
                next_fragment = self.packet.next()
        
                 
            #End of the transmission procedure
            
            ###### Final AoI
            if bs.try_decode(self.packet,env.now) == True:
                #if self.packet.AoI_final==0:
                    self.packet.AoI_final=env.now
                    self.final_timestamp.append(self.packet.AoI_final)
                    self.success_quantity += 1
                
            if bs.try_decode(self.packet,env.now) == False:
               
                self.packet.AoI_final=0
                self.final_timestamp.append(self.packet.AoI_final)    
                 
            ######
           
            self.end_of_transmission()

"Represents the gateway, contains information about the fragments and assesses whether this transmission was successful"
class Base():
    def __init__(self, obw, threshold):
        self.id = id(self)
        self.transmitting = {}
        for channel in range(obw):
            self.transmitting[channel] = []
        self.packets_received = {}
        self.threshold = threshold
        
    def add_packet(self, packet):
        pass

    def add_node(self, id):
        self.packets_received[id] = 0

    def receive_packet(self, fragment):
        self.transmitting[fragment.channel].append(fragment)

    def finish_fragment(self, fragment):
        self.transmitting[fragment.channel].remove(fragment)
        if len(fragment.collided) == 0:
            fragment.success = 1
        fragment.transmitted = 1

    def check_collision(self,fragment):
        for f in self.transmitting[fragment.channel]:
            f.collided.append(fragment)
            fragment.collided.append(f)

    "Attempts to decode the packet according to the fragments that arrived here"
    def try_decode(self,packet,now):
        h_success = sum( ((len(f.collided)==0) and f.transmitted==1) if (f.type=='header') else 0 for f in packet.fragments)
        p_success = sum( ((len(f.collided)==0) and f.transmitted==1) if (f.type=='payload') else 0 for f in packet.fragments)
        success = 1 if ((h_success>0) and (p_success >= self.threshold)) else 0
        if success == 1:

            self.packets_received[packet.node_id] += 1

            return True
        else:
        
            return False
            
