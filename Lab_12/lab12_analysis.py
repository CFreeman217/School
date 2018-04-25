import os, re, numpy as np 
import matplotlib.pyplot as plt 

trial_regex = re.compile(r'''(
    (Lab12_)
    (AL|ST)
    (_tc)
    (\d+)
    (in.txt)
)''', re.VERBOSE)

def main():
    ret_poly = lambda val, eqn : sum([coef*val**(len(eqn)-(index+1)) for index, coef in enumerate(eqn)])
    steel_temp = [None]*14
    steel_disp = [None]*14
    al_fit_deg = 5
    al_temp = [None]*14
    al_disp = [None]*14
    for file_name in os.listdir('.'):
        if file_name.startswith('Lab12'):
            t_data = np.loadtxt(file_name, delimiter='\t', skiprows=1,unpack=True,usecols=1)
            m_temp = np.mean(t_data)
            matches = trial_regex.findall(file_name)
            if matches[0][2] == 'ST':
                steel_temp[int(matches[0][4])] = m_temp
                steel_disp[int(matches[0][4])] = int(matches[0][4])
            elif matches[0][2] == 'AL':
                al_temp[int(matches[0][4])] = m_temp
                al_disp[int(matches[0][4])] = int(matches[0][4])
    al_regress = np.polyfit(al_disp,al_temp,deg=al_fit_deg)
    al_reg_list = [ret_poly(i, al_regress) for i in al_disp]
    plt.plot(steel_disp, steel_temp, label='Steel Thermocouple Reading')
    plt.plot(al_disp, al_temp, label='Aluminum Thermocouple Reading')
    plt.plot(al_disp, al_reg_list, label='{} order polyfit'.format(al_fit_deg),ls=':')
    plt.xlabel('Displacement (inches)')
    plt.ylabel('Mean Temperature')
    plt.title('Rod Temperature and Displacement Data')
    plt.legend()
    plt.grid()
    plt.show()
main()
