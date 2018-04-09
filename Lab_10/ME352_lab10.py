import re
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats, integrate

# Some trial information is stored in the file name
# This regex parses each component out for 8 of the 9 text files in the dataset.
trial_regex = re.compile(r'''(

    (Lab10_)
    (\d+)
    (g_)
    (displacement)?
    (displaceMass)?
    (\d+)?

)''', re.VERBOSE)

def main():
    # Initialize variables to hold calibration data when going through the dataset
    disp_cal = []
    rest_cal = []
    rest_n_cal = 0
    force_cal = []
    trial_mass = 4.204
    # Gravity force
    m_g = 9.81*trial_mass
    # Run through the current file
    for file_name in os.listdir('.'):
        if file_name.startswith('Lab10_'):
            # Gather and parse the dataset into variables
            time, disp_x, accel, force = np.loadtxt(open(file_name),
                                            delimiter='\t',
                                            skiprows=1,
                                            unpack=True,
                                            usecols=(0,1,3,5))
            # disp_x = np.array([i*-1 for i in disp_x])
            # accel = np.array([i*-1 for i in accel])
            # Mean displacement, raw voltage data is fed through the calibration function that converts voltage to mm

            m_disp = lp_801_300(np.mean(disp_x))
            # Mean Acceleration, returned in m/s^2
            m_accel = adxl335(np.mean(accel))
            # Mean Force, Newtons
            m_force = LC105_25(np.mean(force))
        # Gather information about the trial
        trial_info = trial_regex.findall(file_name)
        # Catch the zero data offset used to calibrate the rest of the data
        if file_name == 'Lab10_zero_data.txt':
                disp_offset = m_disp
                accel_offset = m_accel
                force_offset = m_force

        # Avoids indexing errors for the rest of the regex matches
        if trial_info != []:
            # Mass of the weight
            mass = float(trial_info[0][2])/1000
            # Actual trial information
            if trial_info[0][-2] == 'displaceMass':
                trial_no = int(trial_info[0][-1])
                if trial_no == 3:
                    uf_d_x = lp_801_300(disp_x)
                    d_x = butterworth_filter(uf_d_x, 7000, 20)
                    # The acceleration data is noisy, so it needs a filter
                    uf_d_a = adxl335(accel)
                    d_a = butterworth_filter(uf_d_a,5000,20)
                    f_y = LC105_25(force)
                    # Calibration information
            if trial_info[0][-3] == 'displacement':
                force_cal.append(mass*9.81)
                disp_cal.append(m_disp)
                if trial_info[0][2] == '4112':
                    rest_cal.append(m_disp)
                    rest_n_cal += 1

    # #
    # #
    # #
    # # Spring Calibration Data
    # #
    # #
    # #
    rest_cal = sum(rest_cal)/rest_n_cal
    # Displacement calibration offset
    disp_cal = abs(disp_offset-disp_cal)
    # Spring constant using linear fit for calibration data
    s_const_k , y_int = lin_reg(disp_cal, force_cal)
    # Finding boundaries
    cal_min = min(disp_cal)
    cal_max = max(disp_cal)
    # Create axis of points
    cal_xaxis = np.linspace(cal_min, cal_max, 100)
    # Define Linfit function
    cal_linfit_fcn_spring = lambda x : s_const_k *cal_xaxis + y_int
    # Subtract zero offsets
    uf_d_x = rest_cal - uf_d_x
    d_x = rest_cal - d_x
    uf_d_a -= accel_offset
    d_a -= accel_offset
    f_y -= force_offset

    # Method 3: Force data from derived spring constant and potentiometer displacement
    m3_f_data = d_x * s_const_k
    # Method 2: Numeric differentiation of potentiometer data to collect velocity data
    pot_vel = num_1deriv(time, d_x)
    # Method 2: Numeric differentiation of potentiometer data to collect acceleration data
    pot_accel = num_2deriv(time, d_x)
    # Method 4: Numeric integration of accelerometer data by simpson's rules to yield velocity data
    acc_vel = lambda a, b : integrate.simps(d_a[a:b],time[a:b])
    # Method 4: Populates a list of velocity point data
    acc_vel_pts = [acc_vel(0, k+1)*9.81 for k, v in enumerate(time) if k < len(time)-1]
    acc_vel_pts.append(acc_vel(0, len(time))*9.81)
    # Method 4: Numeric integration of accelerometer velocity data to yield displacement data
    acc_disp = lambda a, b : integrate.simps(acc_vel_pts[a:b], time[a:b])
    acc_disp_pts = []
    # Set maximum limit on the numeric integration time
    max_int_time = 2 # seconds
    # Collect the integral
    for k, v in enumerate(time):
        # The displacement should read zero once the trial is over and the spring settles
        # however, due to some leftover residuals after the integration, the
        # displacement graph accumulates. 1.35 seconds is an arbitrary value for zeroing the
        # graph out but works for this problem
        if v < max_int_time:
            acc_disp_pts.append(acc_disp(0, k+1)*9.81)
        else:
            acc_disp_pts.append(0)
            # if k < len(time) - 1:
            #     disp = acc_disp(0, k+1)*9.81
            #     if disp > 0:
            #         acc_disp_pts.append(disp)
            #     else:
            #         acc_disp_pts.append(0)
            # else:
            #     acc_disp_pts.append(acc_disp_pts[k-1])
    # Gather damping coefficient information from each data set.
    b_pot = pot_peak_to_peak(time, d_x, pot_vel, trial_mass)
    # b_pot = 0
    b_acm = acm_peak_to_peak(time, d_a, acc_vel_pts, acc_disp_pts, trial_mass)
    # b_acm = 0
    # Populate the force functions
    # Method 2: Potentiometer derived spring force
    pot_sp_f = np.array([((m_g - b_pot*pot_vel[i] - trial_mass*pot_accel[i]))/(2*(9.81**2))+m_g  for i in range(len(d_x))])
    # Method 4: Accelerometer derived spring force

    acc_sp_f = np.array([(m_g + b_acm*acc_vel_pts[i] + trial_mass*d_a[i]) for i in range(len(d_a))])

    plt.plot(time, uf_d_x, label='Unfiltered Displacement')
    plt.plot(time, d_x, label='Filtered Displacement')
    plt.title('Displacement Data Filtering')
    plt.legend()
    plt.savefig('Lab_10_DisplacementFiltering.png', bbox_inches='tight')
    plt.show()
    plt.plot(time, uf_d_a, label='Unfiltered Acceleration')
    plt.plot(time, d_a, label='Filtered Acceleration')
    plt.title('Accleration Data Filtering')
    plt.legend()
    plt.savefig('Lab_10_AccelerationFiltering.png', bbox_inches='tight')
    plt.show()
    plt.plot(time, f_y, label='Force (N)')
    plt.title('Force data Calibration Check')
    plt.legend()
    plt.savefig('Lab_10_ForceCalibration.png', bbox_inches='tight')
    plt.show()

    plt.scatter(np.array(disp_cal), np.array(force_cal))
    plt.plot(cal_xaxis, cal_linfit_fcn_spring(cal_xaxis), color='r', ls='-.')
    plt.title('Spring Constant Calibration Data')
    plt.xlabel('Displacement (mm)')
    plt.ylabel('Force (N)')
    plt.savefig('Lab_10_SpringConstantCalibration.png', bbox_inches='tight')
    plt.show()

    plt.plot(time, d_x, label='Displacement')
    plt.plot(time, [i/9.81 for i in pot_vel], label='Velocity')
    plt.plot(time, [i/(9.81**2) for i in pot_accel], label='Acceleration')
    plt.title('Potentiometer Data')
    plt.xlabel('Time')
    plt.ylabel('mm, m/s, or m/s^2')
    plt.legend()
    plt.savefig('Lab_10_PotentiometerData.png', bbox_inches='tight')
    plt.show()

    plt.plot(time, acc_disp_pts, label='Displacement')
    plt.plot(time, acc_vel_pts, label='Velocity')
    plt.plot(time, d_a, label='Acceleration')
    plt.title('Accelerometer Data')
    plt.xlabel('Time')
    plt.ylabel('mm, m/s, or m/s^2')
    plt.legend()
    plt.savefig('Lab_10_AccelerometerData.png', bbox_inches='tight')
    plt.show()

    # # # # plt.plot(time, ode_array, label='ODE Integration (Method 1)')
    plt.plot(time, pot_sp_f, label='Potentiometer Differentiation (Method2)')
    plt.plot(time, m3_f_data, label='Spring Constant and Displacement (Method 3)')
    plt.plot(time, acc_sp_f, label='Force from Acceleration (Method 4)')
    plt.plot(time, f_y, label='Force From Load Cell (Direct Measurement)')
    plt.title('Time and Force')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.legend()
    plt.savefig('Lab_10_SpringForceMethods_n.png', bbox_inches='tight')
    plt.show()

def lp_801_300(in_volts):
    '''
    Returns displacement in mm from input voltage on Omega LP801-300 linear potentiometer
    '''
    min_volts = 0
    max_volts = 3 # Volts
    min_travel = 0
    max_travel = 300 # mm
    displacement = abs(in_volts * (max_travel-min_travel) / (max_volts - min_volts))
    # linearity = (max_volts - min_volts) * 0.01
    # hysteresis = 0.025 # mm
    # repeatability = 0.012 # mm
    # error = np.sqrt(linearity**2 + hysteresis**2 + repeatability**2)
    # print('LP801-300 Measurement Results:')
    # print('Measured Displacement : {:1.2f} mm'.format(displacement))
    # print('Uncertainty : +/- {:1.2f} mm'.format(error))
    return displacement

def adxl335(in_volts):
    '''
    Returns acceleration from input voltage to Analog Devices ADXL335 Accelerometer
    '''
    min_volts = 0
    max_volts = 3.6 # Volts
    gravity = 9.80665
    min_g = -3.6
    max_g = 3.6
    min_accel = min_g*gravity
    max_accel = max_g*gravity # m/s^2 with g = 9.80665
    acceleration = (in_volts * (max_accel-min_accel) / (max_volts - min_volts))
    return acceleration

def LC105_25(in_volts):
    '''
    Returns force data from Omega LC105-25 Force sensor
    '''
    min_input = 0
    max_input = 3 # Volts
    min_output = 0
    max_output = 133.4466 # 25 pounds, where 1 lb = 4.44822 N
    output_data = (in_volts * (max_output-min_output) / (max_input - min_input))
    return output_data

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
    y_mean = s_yi/n
    s_xi2 = sum([i**2 for i in x_list])
    s_xy = sum([x_list[i]*y_list[i] for i in range(n)])
    # Calculate coefficients
    coef_a = ((n * s_xy) - (s_xi * s_yi)) / ((n * s_xi2) - (s_xi**2))
    coef_b = ((s_xi2 * s_yi) - (s_xi * s_xy)) / ((n*s_xi2) - (s_xi**2))
    # # Sum of the squares of residuals from the generated line
    # s_sq_t = sum([((coef_a * x_list[i] + coef_b - y_list[i])**2) for i in range(n)])
    # # Sum of the squares of residuals from the mean
    # s_sq_r = sum([(y_list[i] - y_mean)**2 for i in range(n)])
    # # Standard deviation
    # st_dev = (s_sq_r / (n-1))**(0.5)
    # # R-Squared Value - coefficient of determination
    # r_sq = 1 - (s_sq_t / s_sq_r)
    # # Standard error
    # std_er = (s_sq_t/(n-2))**(0.5)
    # # Find maximum error deviation from the best fit line
    # er_max = max([abs(coef_a * x_list[i] + coef_b - y_list[i]) for i in range(n)])
    print('Linear Best Fit: y = ( {:.4f} ) x {:+.4f}'.format(coef_a,coef_b))
    # print('Standard Deviation = {:.4f}'.format(st_dev))
    # print('R-Squared, Calibration Constant = {:.4f}'.format(r_sq))
    # print('Standard Error = {:.4f}'.format(std_er))
    # print('Maximum Error = {:.4f}\n'.format(er_max))
    return coef_a, coef_b

def butterworth_filter(in_data, f_s=10000, f_c=20):
    '''
    Filters input data in butterworth plot to get rid of noise

    f_s : Sampling Frequency for the dataset
    f_c : Cutoff Frequency to eliminate noise
    '''
    W_n = 2 * f_c / f_s # Natural Frequency
    b, a = signal.butter(2, W_n)
    filtered_data = signal.filtfilt(b, a, in_data)
    return filtered_data

def num_1deriv(x_list, y_list):
    '''
    Numerical Methods - Numeric Differentiation of a list of data points
    returns first derivative
    Forward Finite Divided difference at the start, Backward at the end, and centered in the middle
    '''
    st_sz = abs(x_list[0] - x_list[1])
    out_list = []
    n_size = len(y_list)
    for i_x, value in enumerate(y_list):
        if i_x == 0:
            # First data point uses Forward Finite Divided Difference
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            f_deriv = (-p_2 + 4*p_1 - 3*value)/(2*st_sz)

        if i_x == 1 or i_x == n_size-2:
            # The end points do not have as much data so the derivative loses accuracy, fewer series terms available
            p_1 = y_list[i_x+1]
            m_1 = y_list[i_x-1]
            f_deriv = ((p_1) - (m_1))/(2*st_sz)

        elif i_x > 1 and i_x < n_size-2:
            # Centered method while the data exists
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            m_1 = y_list[i_x-1]
            m_2 = y_list[i_x-2]
            f_deriv = (-p_2 + 8*p_1 - 8*m_1 + m_2)/(12*st_sz)

        elif i_x == n_size -1:
            # Last data point uses Backward Finite Divided Difference
            m_2 = y_list[i_x-2]
            m_1 = y_list[i_x-1]
            f_deriv = (m_2 - 4*m_1 + 3*value)/(2*st_sz)

        out_list.append(f_deriv)
    return out_list

def num_2deriv(x_list, y_list):
    '''
    Numerical Methods - Numeric Differentiation of a list of data points
    returns second derivative
    Forward Finite Divided difference at the start, Backward at the end, and centered in the middle
    '''
    st_sz = abs(x_list[0] - x_list[1])
    out_list = []
    n_size = len(y_list)
    for i_x, value in enumerate(y_list):
        if i_x == 0:
            # First data point uses Forward Finite Divided Difference
            p_3 = y_list[i_x+3]
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            f_deriv = (-p_3 + 4*p_2 - 5*p_1 + 2*value)/(st_sz**2)
        if i_x == 1 or i_x == n_size-2:
            # The end points do not have as much data so the derivative loses accuracy, fewer series terms available
            p_1 = y_list[i_x+1]
            m_1 = y_list[i_x-1]
            f_deriv = (p_1 - 2*value + m_1)/(st_sz**2)
        elif i_x > 2 and i_x < n_size-2:
            # Centered method while the data exists
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            m_1 = y_list[i_x-1]
            m_2 = y_list[i_x-2]
            f_deriv = (-p_2 + 16*p_1 - 30*value + 16*m_1 - m_2)/(12*st_sz**2)
        elif i_x == n_size -1:
            # Last data point uses Backward Finite Divided Difference
            m_3 = y_list[i_x-3]
            m_2 = y_list[i_x-2]
            m_1 = y_list[i_x-1]
            f_deriv = (2*value - 5*m_1 + 4*m_2 - m_3)/(st_sz**2)
        out_list.append(f_deriv)
    return out_list

def pot_peak_to_peak(time, disp_data, vel_data, mass):
    '''
    Finds amplitude and time of first two peaks to determine damping coefficient, b
    ** Needs to be adjusted per problem dataset for peaks, requires numpy enabled as np.
    '''
    sign_toggle = 0
    zero_list = []
    # Find where the sign of the velocity data crosses zero. The following is a
    # little toggle switch case that yields the index of these points for the velocity.
    for index, item in enumerate(vel_data):
        sign = sign_toggle
        if item*-1 > 0:
            # Negative
            sign = 0
        else:
            sign = 1
        if sign != sign_toggle:
            zero_list.append(index)
            sign_toggle = sign
    # Picking these peaks is done specific to this problem and this dataset. Would need
    # to be adjusted when using a different set of data.
    # [print('[ {} , {} ]'.format(time[i], disp_data[i])) for i in zero_list]
    peak1 = disp_data[zero_list[1]]
    time1 = time[zero_list[1]]
    peak2 = disp_data[zero_list[3]]
    time2 = time[zero_list[3]]
    dt = time2-time1
    d_const_b = (-2 * mass * np.log(peak2/peak1))/dt
    # print('Damping Constant from Potentiometer Data : {}'.format(d_const_b))
    return d_const_b

def acm_peak_to_peak(time, accel_data, vel_data, disp_data, mass):
    '''
    Generates a damping coefficient from filtered accelerometer data
    '''
    sign_toggle = 0
    vel_zero_list = []
    for index, item in enumerate(vel_data):
        sign = sign_toggle
        if item*-1 > 0:
            # Negative
            sign = 0
        else:
            sign = 1
        if sign != sign_toggle:
            vel_zero_list.append(index)
            sign_toggle = sign
    # [print('[ {} , {} ]'.format(time[i], disp_data[i])) for i in vel_zero_list]
    peak1 = disp_data[vel_zero_list[3]]
    time1 = time[vel_zero_list[3]]
    peak2 = disp_data[vel_zero_list[5]]
    time2 = time[vel_zero_list[5]]
    dt = time2-time1
    d_const_b = (-2 * mass * np.log(peak2/peak1))/dt
    # print('Damping Constant from Accelerometer Data : {}'.format(d_const_b))
    return d_const_b

def mass_spring(state, t, k, m):
    '''
    general solution for simple harmonic motion with damping
    Force equation: d2xdy2 + (omega^2)*x
    Where w[omega] = sqrt(k/m)
    x(t) = Acos(wt) + Bsin(wt)
    x(t) = Ccos(wt - p)
    Where p = phase angle, phi
    '''
    '''
    0 = d2xdt2 + (b/m)*dxdt + (k/m)*x
    alpha[a] = - (b/m) * (dxdt)
    beta[b] = +/- (sqrt(b^2 - 4*k*m)/2m)
    lambda_1 = - a + b
    lambda_2 = - a - b
    x(t) = c_1*e^-((a-b)*t) + c_2*e^-((a+b)*t)

    b^2 > 4*m*k : Overdamping - 2 real roots
    b^2 = 4*m*k : Critical Damping - Repeated roots
    b^2 < 4*m*k : Underdamping
    Frequency of oscillation in underdamped system
    omega_prime[w_p] = sqrt((k/m) - (b^2/4m^2))
    Oscillatory motion
    x(t) = Ae^-((k/2)*t) * cos(w_p*t -p)
    '''
    # unpack the state vector
    x = state[0]
    xd = state[1]

    # these are our constants
    w_2 = (k/m) # omega_squared
    freq = np.sqrt(w_2)/(2*np.pi)
    g = 9.81

    # compute acceleration xdd
    xdd = g - w_2*x

    # return the two state derivatives
    return [xd, xdd]

main()