l_resp = input('Time to respond to input = ')
y_ss = input('Total change in yaw = ')
tau = input('Time to intercept slope against settling value = ')
y_cmd = input('Total Change in cmd = ')

tot_k = float(y_ss)/float(y_cmd)
k_p = 1.2*(float(tau)/(tot_k*float(l_resp)))
t_i = 2*float(l_resp)
t_d = 0.5*float(l_resp)

print(f'K_p = {k_p}\nK_i = {k_p/t_i}\nK_d = {k_p*t_d}')