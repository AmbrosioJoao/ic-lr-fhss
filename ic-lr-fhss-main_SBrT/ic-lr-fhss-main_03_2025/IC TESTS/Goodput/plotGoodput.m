clear all;
close all;

Devices_theo=[1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, ...
60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000, 105000, 110000, 115000, 120000, ...
125000, 130000, 135000, 140000, 145000, 150000];

lambda=900;
l=10;
c=35;
header_duration=0.233472;
payload_duration=0.102400;
transceiver_wait = 0.006472;

for i=1:length(Devices_theo)
    number_nodes=Devices_theo(i)/8;
    [~, Goodput_dr8_theor(i)] = theoretical_DR(number_nodes, 3, header_duration, 1/3, payload_duration, transceiver_wait, c, l, lambda);
    [~, Goodput_dr9_theor(i)] = theoretical_DR(number_nodes, 2, header_duration, 2/3, payload_duration, transceiver_wait, c, l, lambda);
end

%% Figure 1
figure (1);
h=plot(Devices_theo/1000, Goodput_dr8_theor, '-', 'Color', [0.000, 0.447, 0.741], 'MarkerFaceColor', [0.000, 0.447, 0.741], 'LineWidth', 1.5, 'MarkerSize',8);
hold on;
grid on;
plot(Devices_theo/1000, Goodput_dr9_theor, '-', 'Color', [0.635, 0.078, 0.184], 'MarkerFaceColor', [0.635, 0.078, 0.184], 'LineWidth', 1.5, 'MarkerSize',8);
clear plot_legend;

plot_legend(1) = plot(inf, inf, 'o', 'Color', [0.000, 0.447, 0.741], 'MarkerFaceColor', [0.000, 0.447, 0.741], 'MarkerSize',8);
plot_legend(2) = plot(inf, inf, 's', 'Color', [0.301, 0.745, 0.933], 'MarkerFaceColor', [0.301, 0.745, 0.933], 'MarkerSize',8);

l = legend(plot_legend, 'DR8', 'DR9');

grid on;
ylabel('$\mathrm{Goodput}\,\mathrm{[bytes/s]}$','Interpreter','LaTeX','Fontsize',13);
xlabel('$\mathrm{Dispositivos}\,{(M)}$','Interpreter','LaTeX','Fontsize',13);

ax = ancestor(h, 'axes')
ax.XAxis.Exponent = 0
ax.XAxis.TickLabelFormat = '%.0fk'