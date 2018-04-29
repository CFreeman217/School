import os, re, numpy as np, openpyxl as opx
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
    st_fit_deg = 5
    al_temp = [None]*14
    al_disp = [None]*14

    for file_name in os.listdir('.'):
        if file_name.startswith('Lab12'):
            t_data = np.loadtxt(file_name, delimiter='\t', skiprows=1,unpack=True,usecols=1)
            t_data = [i+273.15 for i in t_data]
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
    st_regress = np.polyfit(steel_disp, steel_temp, deg = st_fit_deg)
    st_reg_list = [ret_poly(i, st_regress) for i in steel_disp]

    ex_wkbk = opx.load_workbook('Lab 12.xlsx', data_only=True)
    exal_ir = ex_wkbk['Al IR data']
    alir_data = []
    c_grp = exal_ir['H4:17']
    for item in c_grp:
        alir_data.append(item[0].value)

    exst_ir = ex_wkbk['Steel IR data']
    stir_data = []
    c_grp = exst_ir['H4:17']
    for item in c_grp:
        stir_data.append(item[0].value)

    plt.plot(steel_disp, steel_temp, label='Thermocouple Reading')
    plt.plot(steel_disp, stir_data, label='Infrared Thermometer')
    # plt.plot(steel_disp, st_reg_list, label='{} order polyfit'.format(st_fit_deg),ls=':')
    plt.xlabel('Displacement (inches)')
    plt.ylabel('Mean Temperature (K)')
    plt.title('Figure 1a : Steel Temp Data')
    plt.legend()
    plt.grid()
    plt.savefig('Lab_12_Figure_1a.png',bbox_inches='tight')
    plt.show()

    plt.plot(al_disp, al_temp, label='Thermocouple Reading')
    plt.plot(al_disp, alir_data, label='Infrared Thermometer')
    # plt.plot(al_disp, al_reg_list, label='{} order polyfit'.format(al_fit_deg),ls=':')
    plt.xlabel('Displacement (inches)')
    plt.ylabel('Mean Temperature (K)')
    plt.title('Figure 1b : Aluminum Temp Data')
    plt.legend()
    plt.grid()
    plt.savefig('Lab_12_Figure_1b.png',bbox_inches='tight')
    plt.show()

main()
