% Characteristic eqn for closed loop system
% s^2 + 2s + 25 = 0

w_n_old = sqrt(25);
zeta_old = 2/(2*w_n_old);

os_pcnt = exp(-zeta_old*pi/sqrt(1-zeta_old^2))*100;
t_s = 4/(zeta_old*w_n_old);

os_des = 15; % desired overshoot percent
t_s_des = 0.5; % desired settling time
zeta = (-log(os_des/100)) / sqrt(pi^2 + log(os_des/100)^2);
sigma = 4/t_s_des;
w_n = sigma/zeta;

% T(s) = C(s) / R (s) = (25 * K_1) / (s^2 + (2 + 25 * K_f) * s + 25 * K_1)

K_f = (2*sigma - 2)/ 25;
K_1 = (w_n^2)/25;

e_ss = 1/25/2;

G1_num = 25*K_1;
G1_den2 = 2 + 25*K_f;

e_ss2 = G1_num / G1_den2;

sprintf('G_1(s) = %1.2f / s (s + %d)',G1_num, G1_den2)

