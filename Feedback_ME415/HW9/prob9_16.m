os_pcnt = 20.5;
t_settle = 3;
G = zpk([],[0 0 -4 -12],1);

zeta = (-log(os_pcnt/100)) / sqrt(pi^2 + log(os_pcnt/100)^2);
sigma = 4/t_settle;
w_d = sigma * tan(acos(zeta));
d_poles = (-sigma + w_d*1i);

% Let compensator have zero at 0.01
% G_c(s) = (K(s+0.01) / (s+p))
ang_con = 180 + (angle(d_poles + 0.01) - 2*angle(d_poles) - angle(d_poles + 4) - angle(d_poles + 12))*(180/pi);
p_comp = (w_d / tand(ang_con)) + sigma;

new_gain = -real(((d_poles + p_comp) * d_poles^2 * (d_poles + 4) * (d_poles + 12))/(d_poles + 0.01));

sprintf('G_c(s) = %1.1f (s + 0.01) / s + %1.2f',new_gain, p_comp)

Gc = zpk(-0.01, -p_comp, new_gain);
Tcomp = feedback(Gc*G, 1);
step(Tcomp)
legend('Compensated System')

