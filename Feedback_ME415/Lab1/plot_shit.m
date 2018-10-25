% Open the simulink diagram thing before running this script

% Kpu is empirically derived based on controller output to simulink gains
Kpu = 16;
% Number of oscillation peaks found during one peak signal at 0.6Hz
peaks = 7;
% From the formula
Pu = 0.6/peaks;

% Zeigler Nichols Graph
figure
hold on
Ti = 0.5*Pu;
Td = 0.125*Pu;
Kp = 0.6*Kpu;
Ki = Kp/Ti;
Kd = Kp*Td;
sim('prelab_PID.slx')
plot(Input)
plot(Output)
z_n = Output;
outputString = sprintf('K_p = %1.2f , K_i = %1.2f, K_d = %1.2f', Kp, Ki, Kd);
titleString = sprintf('Zeigler Nichols Gains');
legend('Command Position', outputString)
title(titleString)
xlabel('Time(s)')
ylabel('Response')
hold off

% Tyreus and Luyben Graph
figure
hold on
Ti = 2.2 * Pu;
Td = Pu / 6.3;
Kp = Kpu / 2.2;
Ki = Kp / Ti;
Kd = Kp * Td;
sim('prelab_PID.slx')
plot(Input)
plot(Output)
t_l = Output;
outputString = sprintf('K_p = %1.2f , K_i = %1.2f, K_d = %1.2f', Kp, Ki, Kd);
titleString = sprintf('Tyreus and Luyben Gains');
legend('Command Position', outputString)
title(titleString)
xlabel('Time(s)')
ylabel('Response')
hold off

% Original Proportional Controller Graph
figure
hold on
Kp = 5;
Ki = 0;
Kd = 0;
sim('prelab_PID.slx')
plot(Input)
plot(Output)
outputString = sprintf('Proportional Controller K_p = %d',Kp);
plot(z_n)
plot(t_l)
title('Controller Comparison')
xlabel('Time(s)')
ylabel('Response')
legend('Signal (Command Position)', outputString, 'Zeigler Nichols', 'Tyreus Luyben')
hold off