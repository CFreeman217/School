os_pcnt = 25;
t_settle = 2;

zeta = (-log(os_pcnt/100)) / sqrt(pi^2 + log(os_pcnt/100)^2);
sigma = 4/t_settle;
w_d = sigma * tan(acos(zeta));
s_12 = (-sigma + w_d*1i);

ang_con = -(180 + (-angle(s_12) - angle(s_12 + 4) - angle(s_12 + 6) - angle(s_12 + 10))*(180/pi));
p_comp = (w_d / (tand(ang_con)) + sigma);

gain_pd = -real(s_12 * (s_12 + 4) * (s_12 + 6) * (s_12 + 10) / (s_12 + 2.95));

% G = zpk([],[0 -4 -6 -10],1);
% Gc = zpk([-p_comp],[],[gain_pd]);
% Tc = feedback(Gc*G, 1);
% step(Tc)

gain_pid = -real(s_12^2 * (s_12 + 4) * (s_12 + 6) * (s_12 + 10) / ((s_12 + 2.95) * (s_12 + 0.1)));

sprintf('G_c(s) = %1.1f (s + 0.1)(s + %1.2f) / s',gain_pid, p_comp)

G = zpk([],[0 -4 -6 -10],1);
Gc = zpk([-0.1 -p_comp],[0],[gain_pid]);
Tc = feedback(Gc*G, 1);
step(Tc)
figure
t = 0:0.1:15;
u = t;
y = lsim(Tc,u,t);
plot(t,u,t,y,'r--');
legend('Ramp Input','Ramp Response')
