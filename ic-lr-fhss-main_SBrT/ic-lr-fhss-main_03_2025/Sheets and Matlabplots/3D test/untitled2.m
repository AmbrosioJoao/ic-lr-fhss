% clear all;
close all;

%% Importação de dados gerados pela simulação Python
Goodput1_simulated = [4998.8, 48455.2, 77668.8, 97410.4, 108718.8, ...
                      114624.8, 115288.8, 113380.4, 109056.0, 103690.8, ...
                      96490.0, 90086.0, 83064.4, 75689.2, 68288.0];

AoI1_simulated = [0.38941744, 0.40526592, 0.41988705, 0.43292015, 0.44349586, ...
    0.45202805, 0.45986212, 0.46583213, 0.47115549, 0.47563063, ...
    0.47973704, 0.48267078, 0.48538193, 0.48761696, 0.48948516];

Devices = [1000, 11640, 22280, 32928, 43568, 54208, 64856, 75496, 86136, 96784, 107424, ...
    118064, 128712, 139352, 150000];


x = Goodput1_simulated / 3600;  % Converte para Kbps
y = AoI1_simulated;             % Age of Information (AoI)
z = Devices / 1000;             % Dispositivos em milhares

% Criando uma grade para interpolação
[X, Y ] = meshgrid(x, y);  % Cria uma grade com as variáveis x e y

% Interpolando os valores de z em uma grade
Z = griddata(x, y, z, X, Y, 'cubic');  % Interpolação cúbica

% Criando o gráfico 3D com surf
figure;
surf(X, Y, Z);  % Cria o gráfico de superfície 3D
xlabel('Goodput (Kbps)');
ylabel('Age of Information (AoI)');
zlabel('Number of Devices (milhares)');
title('Superfície 3D de Goodput, AoI e Número de Dispositivos');
colorbar;  % Adiciona uma barra de cores para referência

% Segundo gráfico: Contorno para 45k dispositivos
figure;
contour(X, Y, Z, 45); % Curvas de nível para 50 níveis
xlabel('Goodput (Kbps)');
ylabel('Age of Information (AoI)');
zlabel('Number of Devices (milhares)');
title('Curvas de Nível de Goodput, AoI e Número de Dispositivos');
colorbar;  % Barra de cores
