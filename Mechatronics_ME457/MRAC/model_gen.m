stp_in = 20; % Step input angle
throt = 1.5; 
pitch_mpu_madgwick=1;

OS_pcnt = 15; % Desired overshoot percent
t_settle = 1.25; % Desired settling time

zta = -(log(OS_pcnt/100) / sqrt((pi^2 + log(OS_pcnt/100)^2)));
w_n = 4/(zta*t_settle);

coef_a = 1;
coef_b = 2*zta*w_n;
coef_c = w_n^2;
numer = coef_c;

sim('resp_test.slx')

hold on
plot(step_input)
plot(tfr_resp)