G = zpk([-6],[-2 -3 -5],1);
rlocus(G);
sgrid(1/sqrt(2), 0);
axis([-6 0 -4 4])
[gain, poles] = rlocfind(G);

t_settle = 4/-real(poles(2));
sigma_new = 8/t_settle;
s_new = -sigma_new +sigma_new*1i;

new_angle = ((s_new + 6) / ((s_new + 2)*(s_new + 3)*(s_new + 5)));
contrib = angle(new_angle)*(180/pi);

needed_angle = 180-contrib;
z_c = (sigma_new / tand(needed_angle)) + sigma_new

comp_gain = abs(((s_new + 2)*(s_new + 3)*(s_new + 5)) / ((s_new + 6)*(s_new + z_c)));

close
G2 = zpk([-6 -z_c],[-2 -3 -5],comp_gain);
T2 = feedback(G2, 1);
step(T2)

ess_uncomp = 6*comp_gain / (2*3*5)
ess_comp = 6*comp_gain*z_c / (2*3*5)