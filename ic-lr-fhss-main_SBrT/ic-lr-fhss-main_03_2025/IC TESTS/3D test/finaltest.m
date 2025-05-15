% clear all;
close all;

% Lê o arquivo .csv
T = readtable('Goodput_nodes.csv');

%% Importação de dados gerados pela simulação Python
Goodput1_simulated = [4998.8, 48455.2, 77668.8, 97410.4, 108718.8, ...
                      114624.8, 115288.8, 113380.4, 109056.0, 103690.8, ...
                      96490.0, 90086.0, 83064.4, 75689.2, 68288.0];

AoI1_simulated = [0.38941744, 0.40526592, 0.41988705, 0.43292015, 0.44349586, ...
    0.45202805, 0.45986212, 0.46583213, 0.47115549, 0.47563063, ...
    0.47973704, 0.48267078, 0.48538193, 0.48761696, 0.48948516];

Devices = [1000, 11640, 22280, 32928, 43568, 54208, 64856, 75496, 86136, 96784, 107424, ...
    118064, 128712, 139352, 150000];

% Cálculos teóricos para Goodput (como você já havia feito)
Devices_theo = [1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, ...
    60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000, 105000, 110000, 115000, 120000, ...
    125000, 130000, 135000, 140000, 145000, 150000];

lambda = 900;
l = 10;
c = 35;
header_duration = 0.233472;
payload_duration = 0.102400;
transceiver_wait = 0.006472;

% Cálculos teóricos para Goodput
for i = 1:length(Devices_theo)
   number_nodes = Devices_theo(i)/8;
   [Ps1_theor(i), Goodput1_theor(i)] = theoretical_DR(number_nodes, 1, header_duration, 5/6, payload_duration, transceiver_wait, c, l, lambda);
end


x = Goodput1_simulated / 3600;  % Converte para Kbps
y = AoI1_simulated;             % Age of Information (AoI)
z = Devices / 1000;             % Dispositivos em milhares



% Criando o gráfico 3D
figure;
plot3(x, y, z, 'o-', 'Color', [0 0.4470 0.7410], 'MarkerFaceColor', [0 0.4470 0.7410], 'LineWidth', 1.5, 'MarkerSize', 8);

% Configurações do gráfico
title('Relação entre Goodput, AoI e Número de Dispositivos', 'FontSize', 14);
xlabel('$\mathrm{Goodput}\,{(Kbps)}$', 'Interpreter', 'LaTeX', 'FontSize', 13);
ylabel('$\mathrm{AoI}$', 'Interpreter', 'LaTeX', 'FontSize', 13);
zlabel('$\mathrm{Dispositivos}\,{(K)}$', 'Interpreter', 'LaTeX', 'FontSize', 13);

grid on;
view(3); % Visualização 3D
rotate3d on; % Permite girar o gráfico com o mouse

% Verificação dos tamanhos (opcional, apenas para debug)
disp(['Tamanho de x: ', num2str(length(x))]);
disp(['Tamanho de y: ', num2str(length(y))]);
disp(['Tamanho de z: ', num2str(length(z))]);