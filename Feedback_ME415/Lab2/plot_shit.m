% Open the simulink diagram thing before running this script

% Zeigler Nichols Graph
clear
Kp = 6;
Ki = 0;
Kd = 0;
f_in = .5;

decibel = @(x) 20*log10(x);

while (f_in < 20)
fig = figure;
hold on    
savestring = sprintf('freq_plot%1.1f.png',f_in);
sim('prelab_PID.slx')
plot(Input)
plot(Output)
z_n = Output;

titleString = sprintf('Frequency = %1.2f', f_in);
legend('Command Position', 'Actual Position')
title(titleString)
xlabel('Time(s)')
ylabel('Response')
saveas(fig,savestring);
% hold off;
% close


datastring = sprintf('freq_data_%1.1f.csv',f_in);
T = table(Time.Time,Input.Data,Output.Data,Voltage.Data);
% writetable(T,datastring);
a = 'Time';
b = 'Input';
c = 'Output';
d = 'Voltage';
headers = (a,b,c,d);

xlsxwrite(datastring,headers);
xlsxwrite(datastring,Time.Time, Input.Data, Output.Data, Voltage.Data);
f_in = f_in +19.5;
end
% Tyreus and Luyben Graph
% figure
% hold on
% Ti = 2.2 * Pu;
% Td = Pu / 6.3;
% Kp = Kpu / 2.2;
% Ki = Kp / Ti;
% Kd = Kp * Td;
% sim('prelab_PID.slx')
% plot(Input)
% plot(Output)
% t_l = Output;
% outputString = sprintf('K_p = %1.2f , K_i = %1.2f, K_d = %1.2f', Kp, Ki, Kd);
% titleString = sprintf('Tyreus and Luyben Gains');
% legend('Command Position', outputString)
% title(titleString)
% xlabel('Time(s)')
% ylabel('Response')
% hold off
% 
% Original Proportional Controller Graph
% figure
% hold on
% Kp = 5;
% Ki = 0;
% Kd = 0;
% sim('prelab_PID.slx')
% plot(Input)
% plot(Output)
% outputString = sprintf('Proportional Controller K_p = %d',Kp);
% plot(z_n)
% plot(t_l)
% title('Controller Comparison')
% xlabel('Time(s)')
% ylabel('Response')
% legend('Signal (Command Position)', outputString, 'Zeigler Nichols', 'Tyreus Luyben')
% hold off