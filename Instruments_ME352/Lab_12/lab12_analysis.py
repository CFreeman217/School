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
    t_inf = 23.36+273.15 # Mean room temperature (Kelvin)
    t_boil = 373.15    # Boiling Temperature (Kelvin)
    al_diam = 12.91e-3  # Aluminum rod diameter (meters)
    st_diam = 12.91e-3  # Steel rod diameter (meters)
    al_peri = np.pi*al_diam # Aluminum rod perimeter
    st_peri = np.pi*st_diam # Steel rod perimeter
    al_area = 130.293e-6 # Aluminum cross section area (meters^2)
    st_area = 130.901e-6 # Steel cross section area (meters^2)
    # tc_ball_diam = 2.34e-3 # Thermocouple solder ball diameter (meters)
    # tc_ball_vol = (4/3)*np.pi*(tc_ball_diam/2)**3 # Solder ball volume (meters^3)
    h_rta = 1315.6 / (1000**2) # W/(m^2C) Heat transfer coefficient for room temp air
    # h_bw = 316.47 # Heat transfer coefficient for boiling water

    t_ratio = lambda x : np.log((x-t_inf)/(t_boil - t_inf)) # Nat. log of temp ratio theta
    ret_poly = lambda val, eqn : sum([coef*val**(len(eqn)-(index+1)) for index, coef in enumerate(eqn)])
    # Initialize variables to hold thermocouple temp and displacement info
    steel_temp = [None]*14
    steel_disp = [None]*14
    al_temp = [None]*14
    al_disp = [None]*14

    # Gather thermocouple reading data

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
    
    # Gather excel file info

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

    # Figure 2 Calculations : Temperature ratio vs Distance

    theta_al_tc = [t_ratio(i) for i in al_temp]
    theta_st_tc = [t_ratio(i) for i in steel_temp]
    theta_al_ir = [t_ratio(i) for i in alir_data]
    theta_st_ir = [t_ratio(i) for i in stir_data]

    m_al_ir, _ = lin_reg(al_disp, theta_al_ir)
    m_al_tc, _ = lin_reg(al_disp, theta_al_tc)
    m_st_ir, _ = lin_reg(steel_disp, theta_st_ir)
    m_st_tc, _ = lin_reg(steel_disp, theta_st_tc)

    k_al_ir = (h_rta * al_peri) / ((m_al_ir**2)*al_area)
    k_al_tc = (h_rta * al_peri) / ((m_al_tc**2)*al_area)
    k_st_ir = (h_rta * st_peri) / ((m_st_ir**2)*st_area)
    k_st_tc = (h_rta * st_peri) / ((m_st_tc**2)*st_area)

    q_al_ir = ((h_rta*al_peri*k_al_ir)**(0.5))*(t_boil - t_inf)
    q_al_tc = ((h_rta*al_peri*k_al_tc)**(0.5))*(t_boil - t_inf)
    q_st_ir = ((h_rta*st_peri*k_st_ir)**(0.5))*(t_boil - t_inf)
    q_st_tc = ((h_rta*st_peri*k_st_tc)**(0.5))*(t_boil - t_inf)
    
    eff = lambda q, a : (q)/(h_rta*a*(t_boil - t_inf)*(1000**2))

    eps_al_ir = eff(q_al_ir, al_area)
    eps_al_tc = eff(q_al_tc, al_area)
    eps_st_ir = eff(q_st_ir, st_area)
    eps_st_tc = eff(q_st_tc, st_area)

    nu_al_ir = eff(q_al_ir, al_peri*(14/25.4/1000))
    nu_al_tc = eff(q_al_tc, al_peri*(14/25.4/1000))
    nu_st_ir = eff(q_st_ir, st_peri*(14/25.4/1000))
    nu_st_tc = eff(q_st_tc, st_peri*(14/25.4/1000))

    print('Trendline Slopes:\n')
    print('Aluminum IR Trendline Slope : {}'.format(-m_al_ir))
    print('Aluminum TC Trendline Slope : {}'.format(-m_al_tc))
    print('Steel IR Trendline Slope : {}'.format(-m_st_ir))
    print('Steel TC Trendline Slope : {}'.format(-m_st_tc))
    print('\nConduction Heat Transfer Coefficients: \n')
    print('Aluminum IR K (w/m^2C) : {}'.format(k_al_ir))
    print('Aluminum TC K (w/m^2C) : {}'.format(k_al_tc))
    print('Steel IR K (w/m^2C) : {}'.format(k_st_ir))
    print('Steel TC K (w/m^2C) : {}'.format(k_st_tc))
    print('\nConduction Heat Transfer Rates: \n')
    print('Aluminum IR q (w/m^2) : {}'.format(q_al_ir))
    print('Aluminum TC q (w/m^2) : {}'.format(q_al_tc))
    print('Steel IR q (w/m^2) : {}'.format(q_st_ir))
    print('Steel TC q (w/m^2) : {}'.format(q_st_tc))
    print('\nFin Effectiveness : \n')
    print('Aluminum IR epsilon : {}'.format(eps_al_ir))
    print('Aluminum TC epsilon : {}'.format(eps_al_tc))
    print('Steel IR epsilon : {}'.format(eps_st_ir))
    print('Steel TC epsilon : {}'.format(eps_st_tc))
    print('\nFin Efficiency : \n')
    print('Aluminum IR nu: {}'.format(nu_al_ir))
    print('Aluminum TC nu : {}'.format(nu_al_tc))
    print('Steel IR nu : {}'.format(nu_st_ir))
    print('Steel TC nu : {}'.format(nu_st_tc))

    # Figure 1a : Aluminum Temp vs. Distance

    # plt.plot(al_disp, al_temp, label='Thermocouple Reading')
    # plt.plot(al_disp, alir_data, label='Infrared Thermometer')
    # plt.xlabel('Displacement (inches)')
    # plt.ylabel('Mean Temperature (K)')
    # plt.title('Figure 1a : Aluminum Temp Data')
    # plt.legend()
    # plt.grid()
    # # plt.savefig('Lab_12_Figure_1a.png',bbox_inches='tight')
    # plt.show()

    # # Figure 1b : Steel Temp vs. Distance

    # plt.plot(steel_disp, steel_temp, label='Thermocouple Reading')
    # plt.plot(steel_disp, stir_data, label='Infrared Thermometer')
    # plt.xlabel('Displacement (inches)')
    # plt.ylabel('Mean Temperature (K)')
    # plt.title('Figure 1b : Steel Temp Data')
    # plt.legend()
    # plt.grid()
    # # plt.savefig('Lab_12_Figure_1b.png',bbox_inches='tight')
    # plt.show()

    # plt.plot(al_disp, theta_al_tc, label='Thermocouple')
    # plt.plot(al_disp, theta_al_ir, label='IR Thermometer')
    # plt.xlabel('Displacement (in.)')
    # plt.ylabel('Ln($\Theta$)')
    # plt.title('Figure 2a : Aluminum Theta Data')
    # plt.legend()
    # plt.savefig('Lab_12_Figure_2a.png',bbox_inches='tight')    
    # plt.show()

    # plt.plot(steel_disp, theta_st_tc, label='Thermocouple')
    # plt.plot(steel_disp, theta_st_ir, label='IR Thermometer')
    # plt.xlabel('Displacement (in.)')
    # plt.ylabel('Ln($\Theta$)')
    # plt.title('Figure 2b : Steel Theta Data')
    # plt.legend()
    # plt.savefig('Lab_12_Figure_2b.png',bbox_inches='tight')
    # plt.show()

def lin_reg(x_list, y_list):
    '''
    Generates linear regression best fit line for list of x-values and y-values passed in the form of a list
    Returns coefficients for the form y = a * x + b
    a, b, r_squared, std_er, er_max = lin_fit(x_list, y_list)
    a : a-coefficient
    b : intercept offset
    r_squared : correlation coefficient
    std_er : standard error
    er_max : maximum error
    '''
    # Gather information about the data set
    n = len(x_list)
    if n != len(y_list):
        print('Lists must be of equal length.')
        return
    s_xi = sum(x_list)
    s_yi = sum(y_list)
    s_xi2 = sum([i**2 for i in x_list])
    s_xy = sum([x_list[i]*y_list[i] for i in range(n)])
    # Calculate coefficients
    coef_a = ((n * s_xy) - (s_xi * s_yi)) / ((n * s_xi2) - (s_xi**2))
    coef_b = ((s_xi2 * s_yi) - (s_xi * s_xy)) / ((n*s_xi2) - (s_xi**2))

    return coef_a, coef_b

main()
