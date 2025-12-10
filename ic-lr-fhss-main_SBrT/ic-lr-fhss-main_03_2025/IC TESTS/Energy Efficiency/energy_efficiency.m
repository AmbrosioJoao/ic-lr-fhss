
%% Importação
EE1_simulated = table2array(EE_case1)';
EE2_simulated = table2array(EE_case2)';
EE3_simulated = table2array(EE_case3)';
EE4_simulated = table2array(EE_case4)';

Devices= [1000, 8842, 16684, 24526, 32368, 40211, 48053, 55895, 63737, 71579, ...
79421, 87263, 95105, 102947, 110789, 118632, 126474, 134316, 142158, 150000]

Devices_theo=[1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, ...
60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000, 105000, 110000, 115000, 120000, ...
125000, 130000, 135000, 140000, 145000, 150000];

lambda=900;
l=10;
c=35;
header_duration=0.233472;
payload_duration=0.100;
transceiver_wait = 0.006472;
tx_power = 0.01;
headers=[1 1 2 2 3 3];


for i=1:length(Devices_theo)
   number_nodes=Devices_theo(i)/8;
  [EE1_theor(i)] = theoretical_DR_ee(number_nodes, 1, header_duration, 5/6, payload_duration, transceiver_wait, c, l, lambda, tx_power);
  [EE2_theor(i)] = theoretical_DR_ee(number_nodes, 2, header_duration, 2/3, payload_duration, transceiver_wait, c, l, lambda, tx_power);
  [EE3_theor(i)] = theoretical_DR_ee(number_nodes, 2, header_duration, 1/2, payload_duration, transceiver_wait, c, l, lambda, tx_power);
  [EE4_theor(i)] = theoretical_DR_ee(number_nodes, 3, header_duration, 1/3, payload_duration, transceiver_wait, c, l, lambda, tx_power);
end

%% Figure 1

%%
figure (1);

h=plot(Devices/1000, EE1_simulated, 'o', 'Color', [0 0.4470 0.7410], 'MarkerFaceColor', [0 0.4470 0.7410], 'LineWidth', 1.5, 'MarkerSize',8);
hold on;
grid on;

plot(Devices_theo/1000, EE1_theor, '-', 'Color', [0 0.4470 0.7410], 'MarkerFaceColor', [0 0.4470 0.7410], 'LineWidth', 1.5, 'MarkerSize',8);
plot(Devices/1000, EE2_simulated, 's', 'Color', [0.8500 0.3250 0.0980], 'MarkerFaceColor', [0.8500 0.3250 0.0980], 'LineWidth', 1.5, 'MarkerSize',8);
plot(Devices_theo/1000, EE2_theor, '-', 'Color', [0.8500 0.3250 0.0980], 'MarkerFaceColor', [0 0.4470 0.7410], 'LineWidth', 1.5, 'MarkerSize',8);
plot(Devices/1000, EE3_simulated, 'd', 'Color', [0.9290 0.6940 0.1250], 'MarkerFaceColor', [0.9290 0.6940 0.1250], 'LineWidth', 1.5, 'MarkerSize',8);
plot(Devices_theo/1000, EE3_theor, '-', 'Color', [0.9290 0.6940 0.1250], 'MarkerFaceColor', [0.9290 0.6940 0.1250], 'LineWidth', 1.5, 'MarkerSize',8);
plot(Devices/1000, EE4_simulated, '^', 'Color', [0.4940 0.1840 0.5560], 'MarkerFaceColor', [0.4940 0.1840 0.5560], 'LineWidth', 1.5, 'MarkerSize',8);
plot(Devices_theo/1000, EE4_theor, '-', 'Color', [0.4940 0.1840 0.5560], 'MarkerFaceColor', [0.4940 0.1840 0.5560], 'LineWidth', 1.5, 'MarkerSize',8);

clear plot_legend;

plot_legend(1) = plot(inf, inf, 'o', 'Color', [0 0.4470 0.7410], 'MarkerFaceColor', [0 0.4470 0.7410], 'MarkerSize',8);
plot_legend(2) = plot(inf, inf, 's', 'Color', [0.8500 0.3250 0.0980], 'MarkerFaceColor', [0.8500 0.3250 0.0980], 'MarkerSize',8);
plot_legend(3) = plot(inf, inf, 'd', 'Color', [0.9290 0.6940 0.1250], 'MarkerFaceColor', [0.9290 0.6940 0.1250], 'MarkerSize',8);
plot_legend(4) = plot(inf, inf, '^', 'Color', [0.4940 0.1840 0.5560], 'MarkerFaceColor', [0.4940 0.1840 0.5560], 'MarkerSize',8);
plot_legend(5) = plot(inf, inf, '-', 'Color', 'k');

l = legend(plot_legend, 'h:1 - CR:5/6', 'h:2 - CR:2/3', 'h:2 - CR:1/2', 'h:3 - CR:1/3', 'Teórico','Fontsize',11);

grid on;
ylabel('$\mathrm{Energy Efficiency}$','Interpreter','LaTeX','Fontsize',13);
xlabel('$\mathrm{Dispositivos}\,{(K)}$','Interpreter','LaTeX','Fontsize',13);

ax = ancestor(h, 'axes')
ax.XAxis.Exponent = 0
ax.XAxis.TickLabelFormat = '%.0fk'