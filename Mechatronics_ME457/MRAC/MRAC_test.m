gam_pcmd = .1;
gam_p = 5;

OS_pcnt = 15; % Desired overshoot percent
t_settle = 1.25; % Desired settling time

zta = -(log(OS_pcnt/100) / sqrt((pi^2 + log(OS_pcnt/100)^2)));
w_n = 4/(zta*t_settle);
% Coefficient calculation
coef_a = 1;
coef_b = 2*zta*w_n;
coef_c = w_n^2;
% Reference model
ref_num = [coef_c];
ref_den = [coef_a coef_b coef_c];
% Dynamic model
dyn_num = [18];
dyn_den = [1 20 56];
k_p = 0.0038;
k_i = 0;
k_d = 0.00073;
% sim('MRAC_PIDresp.slx')

% hold on
% plot(step_input)
% plot(pitch_out)