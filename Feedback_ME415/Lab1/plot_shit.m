hold on
plot(Input)
for Kp=2:4:10
    sim('prelab_PID.slx')
    plot(Output) 
end
plot(Output)
titleString = sprintf('Proportional Gain Response');
legend('Command Position', 'K_p = 2', 'K_p = 6', 'K_p = 10')
title(titleString)
xlabel('Time(s)')
ylabel('Response')