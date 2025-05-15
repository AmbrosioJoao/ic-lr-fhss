% clear all;
close all;

%% Importação de dados gerados pela simulação Python
Goodput4_simulated = [4963.6, 57648.4, 107245.6, 148914.0, 179694.0, ...
                 197660.8, 202448.4, 195756.0, 180567.6, 160605.6, ...
                 138232.4, 115278.4, 93929.6, 74868.4, 58481.6];


AoI4_simulated = [0.38571533, 0.38774349, 0.39093129, 0.39786323, ...
                  0.40709269, 0.41775513, 0.4296039, 0.44203149, ...
                  0.45284087, 0.46273692, 0.47103058, 0.47796653, ...
                  0.48349514, 0.48781065, 0.49139029];

Devices = [1000, 11640, 22280, 32928, 43568, 54208, 64856, 75496, 86136, 96784, 107424, ...
    118064, 128712, 139352, 150000];


x = Goodput4_simulated / 3600;  % Converte para Kbps
y = AoI4_simulated;             % Age of Information (AoI)
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
