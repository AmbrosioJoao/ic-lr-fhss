% clear all;
close all;

% Lê o arquivo .csv
T = readtable('Goodput_nodes.csv');


%% Importação de dados gerados pela simulação Python
Goodput1_simulated = str2double(T.Goodput_case1)';

AoI1_simulated = [0.38941744, 0.40526592, 0.41988705, 0.43292015, 0.44349586, ...
    0.45202805, 0.45986212, 0.46583213, 0.47115549, 0.47563063, ...
    0.47973704, 0.48267078, 0.48538193, 0.48761696, 0.48948516];


Devices = [1000, 11640, 22280, 32928, 43568, 54208, 64856, 75496, 86136, 96784, 107424, ...
    118064, 128712, 139352, 150000];

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

%% Figura 1: Goodput (Simulado vs Teórico)

% Criação de uma figura com 2 subgráficos
figure;

% Subgráfico 1 (Goodput)
subplot(2, 1, 1); % Divide a figura em 2 linhas e 1 coluna, e seleciona o primeiro subgráfico

% Plot do gráfico de Goodput
h = plot(Devices/1000, Goodput1_simulated/3600, 'o', 'Color', [0 0.4470 0.7410], 'MarkerFaceColor', [0 0.4470 0.7410], 'LineWidth', 1.5, 'MarkerSize', 8);
hold on;
grid on;
plot(Devices_theo/1000, Goodput1_theor, '-', 'Color', [0 0.4470 0.7410], 'MarkerFaceColor', [0 0.4470 0.7410], 'LineWidth', 1.5, 'MarkerSize', 8);

% Configurações para o gráfico de Goodput
ylabel('$\mathrm{Goodput}$', 'Interpreter', 'LaTeX', 'Fontsize', 13);
xlabel('$\mathrm{Dispositivos}\,{(K)}$', 'Interpreter', 'LaTeX', 'Fontsize', 13);
legend('Simulado', 'Teórico', 'FontSize', 11);
ax = ancestor(h, 'axes');
ax.XAxis.Exponent = 0;
ax.XAxis.TickLabelFormat = '%.0fk';

% Subgráfico 2 (AoI)
subplot(2, 1, 2); % Seleciona o segundo subgráfico

% Plot do gráfico de AoI
h = plot(Devices/1000, AoI1_simulated, 'o-', 'Color', [0 0.4470 0.7410], 'MarkerFaceColor', [0 0.4470 0.7410], 'LineWidth', 1.5, 'MarkerSize', 8);
hold on;

% Configurações para o gráfico de AoI
ylabel('$\mathrm{AoI}$', 'Interpreter', 'LaTeX', 'Fontsize', 13);
xlabel('$\mathrm{Dispositivos}\,{(K)}$', 'Interpreter', 'LaTeX', 'Fontsize', 13);
legend('Simulado', 'FontSize', 11);
ax = ancestor(h, 'axes');
ax.XAxis.Exponent = 0;
ax.XAxis.TickLabelFormat = '%.0fk';


