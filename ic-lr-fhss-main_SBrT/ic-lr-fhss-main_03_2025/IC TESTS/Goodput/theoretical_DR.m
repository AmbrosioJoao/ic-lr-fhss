function [PacketSuccessProbability,...
          Goodput] = theoretical_DR(devices, headers, header_duration, CR, payload_duration, transceiver_wait, c, l, lambda)
%==========================================================================

%==========================================================================
f=ceil((l+3)/(6*CR));
threshold=ceil(f*CR);

u_H=(devices*headers)/lambda;
u_F = (devices*f)/lambda;
A_H=max(1, u_H*2*header_duration+u_F*(header_duration+payload_duration+transceiver_wait));

P_H = 1 - (1-(1-(1/c))^(A_H-1))^headers;

A_F = max(1, u_F*2*payload_duration + u_H*(header_duration+payload_duration+transceiver_wait));
p_F = (1-(1/c))^(A_F-1);

range = 1:1:threshold;
aux=0;
    
for k=1:length(range)
   loop=k-1;
   aux=aux+nchoosek(f, loop)*(p_F^loop)*(1-p_F)^(f-loop);
end
P_F = 1 - aux;
PacketSuccessProbability=(P_F.*P_H);
Goodput=(PacketSuccessProbability*l*devices*(1/lambda));