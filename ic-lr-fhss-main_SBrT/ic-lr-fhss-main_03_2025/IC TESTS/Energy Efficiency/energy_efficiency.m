close all;

%% Importação
EE1_simulated = table2array(EE_case1)';
EE2_simulated = table2array(EE_case2)';
EE3_simulated = table2array(EE_case3)';
EE4_simulated = table2array(EE_case4)';

Devices = [1000, 8840, 16680, 24520, 32368, 40208, 48048, 55888, 63736, 71576, ...
    79416, 87256, 95096, 102944, 110784, 118624, 126472, 134312, 142152, 150000];


%% Figura
figure(1);
hold on;
grid on;

% Curvas simuladas com marcadores + linhas mais grossas
h1 = plot(Devices/1000, EE1_simulated, '-s', 'Color', [0.8500 0.3250 0.0980], ...
    'MarkerFaceColor', [0.8500 0.3250 0.0980], 'LineWidth', 2, 'MarkerSize',8);

h2 = plot(Devices/1000, EE2_simulated, '-d', 'Color', [0.9290 0.6940 0.1250], ...
    'MarkerFaceColor', [0.9290 0.6940 0.1250], 'LineWidth', 2, 'MarkerSize',8);

h3 = plot(Devices/1000, EE3_simulated, '-^', 'Color', [0.4940 0.1840 0.5560], ...
    'MarkerFaceColor', [0.4940 0.1840 0.5560], 'LineWidth', 2, 'MarkerSize',8);

h4 = plot(Devices/1000, EE4_simulated, '-o', 'Color', [0 0.4470 0.7410], ...
    'MarkerFaceColor', [0 0.4470 0.7410], 'LineWidth', 2, 'MarkerSize',8);

% Legenda usando os próprios handles
legend([h1 h2 h3 h4], ...
    'h:1 - CR:5/6', ...
    'h:2 - CR:2/3', ...
    'h:2 - CR:1/2', ...
    'h:3 - CR:1/3', ...
    'FontSize',11, 'Location','best');

% Eixos
xlabel('Dispositivos (K)','Interpreter','tex','FontSize',13);
ylabel('Eficiência Energética (ε)','Interpreter','tex','FontSize',13);
ax = ancestor(h1, 'axes');
ax.XAxis.Exponent = 0;
ax.XAxis.TickLabelFormat = '%.0fk';
