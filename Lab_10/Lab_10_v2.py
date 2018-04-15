import re
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, integrate

# Some trial information is stored in the file name
# This regex parses each component out for 8 of the 9 text files in the dataset.
trial_regex = re.compile(r'''(

    (Lab10_)
    (\d+)
    (g_)
    (displacement|displaceMass)
    (\d+|_\d+)?

)''', re.VERBOSE)

def main():
    trial_mass = 4.112
    m_g = 9.81*trial_mass
    # Initialize variables to hold calibration data when going through the dataset
    # Displacement calibration values for each mass and spring condition
    disp_cal = []
    # resting data at the bouncing mass. Used to set accelerometer data
    rest_cal = []
    rest_n_cal = 0
    force_cal = [0]
    f_cal_val = [0]
    c_points = None
    #
    #
    #
    # DATA COLLECTION
    #
    #
    #
    # Run through the current file
    for file_name in os.listdir('.'):
        if file_name.startswith('Lab10_') and file_name.endswith('.txt'):
            # Gather and parse the dataset into variables
            time, disp_x, accel, force = np.loadtxt(open(file_name),
                                            delimiter='\t',
                                            skiprows=1,
                                            unpack=True,
                                            usecols=(0,1,3,5))
            # Mean displacement, raw voltage data is fed through the calibration function that converts voltage to mm
            m_disp = lp_801_300(np.mean(disp_x))
            # Mean Acceleration, returned in m/s^2
            m_accel = adxl335(np.mean(accel))
            # Mean Force, Newtons
            m_force = np.mean(force)
            if c_points == None:
                c_points = len(time)
            elif c_points < len(time):
                c_points = len(time)
            time = np.array([time[i] for i in range(c_points)])
        # Gather information about the trial
        trial_info = trial_regex.findall(file_name)
        # Catch the zero data offset used to calibrate the rest of the data
        if file_name.startswith('Lab10_zero_data.txt'):
                disp_offset = m_disp
                accel_offset = m_accel
                force_offset = m_force
        # Avoids indexing errors for the rest of the regex matches
        if trial_info != []:
            # Mass of the weight
            mass = float(trial_info[0][2])/1000
            # Actual trial information
            if trial_info[0][4] == 'displaceMass':
                trial_no = int(trial_info[0][-1])
                if trial_no == 3:
#
#
#
#   FILTERING AND TRIAL DATA GATHERING
#
#
#
                    d_x = np.array([lp_801_300(disp_x[i]) for i in range(c_points)])
                    d_a = np.array([adxl335(accel[i]) for i in range(c_points)])
                    f_y = [force[i] for i in range(c_points)]
                    # swap = d_a
                    # uf_d_a = d_x
                    # uf_d_x = swap
                    uf_d_a = d_a
                    uf_d_x = d_x
                    d_x = butterworth_filter(uf_d_x, 10000, 30)
                    # The acceleration data is noisy, so it needs a filter
                    d_a = butterworth_filter(uf_d_a, 10000, 20)
                    # Calibration information
            if trial_info[0][4] == 'displacement':
                # Since we know the mass, we can store the applied force for the static tests
                force_cal.append(mass*9.80665)
                # Store the force calibration information because the output from that sensor sucks
                f_cal_val.append(m_force)
                # Store the potentiometer displacement mean for the trial to calibrate the spring
                disp_cal.append(m_disp)
                # This is in case we have more than one static trial dataset where the mass is the same
                # as the bouncing mass.
                if abs(mass - trial_mass) < .5:
                    rest_cal.append(m_disp)
                    rest_n_cal += 1
    #
    #
    #
    # OFFSETS AND CALIBRATION
    #
    #
    #
    # LOAD CELL
    # We generated the force offset data from the zero data information
    # this should go in the first data point of the force calibration values
    f_cal_val[0] = force_offset
    lcell_cal_coef, lc_rsq = lin_origin(force_cal, f_cal_val)
    lcell_cal_list = np.array([lcell_cal_coef * i for i in force_cal])
    f_y = np.array([i/lcell_cal_coef for i in f_y])
    # get rid of the manually entered force cal data point to avoid problems later

    # POTENTIOMETER
    # This is a list containing mean potentiometer readings from displacement trials
    # that were performed at or near the trial mass.
    rest_cal = sum(rest_cal)/rest_n_cal
    # Displacement calibration offset
    disp_cal = abs(disp_offset-disp_cal)
    # Spring constant using linear fit for calibration data.
    # s_const_k , y_int, sc_rsq = lin_reg(disp_cal, force_cal[1:])
    s_const_k , sc_rsq = lin_origin(disp_cal, force_cal[1:])
    # Finding boundaries
    cal_min = min(disp_cal)
    cal_max = max(disp_cal)
    # Create axis of points to plot line best fit
    cal_xaxis = np.linspace(cal_min, cal_max, 2)
    # Define Linfit function
    # cal_linfit_fcn_spring = lambda x : s_const_k *cal_xaxis + y_int
    cal_linfit_fcn_spring = lambda x : s_const_k *cal_xaxis

    # Subtract zero offsets

    # uf_d_x = rest_cal - uf_d_x
    # d_x = rest_cal - d_x
    uf_d_a -= accel_offset
    d_a -= accel_offset
    uf_d_x -= rest_cal
    d_x -= rest_cal
    # uf_d_a = accel_offset - uf_d_a
    # d_a = accel_offset - d_a


    # Method 3: Force data from derived spring constant and potentiometer displacement
    m3_f_data = d_x * s_const_k
    # Method 2: Numeric differentiation of potentiometer data to collect velocity data
    pot_vel = num_1deriv(time, d_x)
    # Method 2: Numeric differentiation of potentiometer data to collect acceleration data
    pot_accel = num_2deriv(time, d_x)
    pot_peaks = findpeaks(time, d_x, pot_vel, pot_accel)
    pp_times = [time[i] for i in pot_peaks]
    pp_data = [d_x[i] for i in pot_peaks]
    # Method 4: Numeric integration of accelerometer data by simpson's rules to yield velocity data
    acc_vel = lambda a, b : integrate.simps(d_a[a:b],time[a:b])
    # Method 4: Populates a list of velocity point data
    acc_vel_pts = [acc_vel(0, k+1)*9.81 for k, v in enumerate(d_a)]
    # Method 4: Numeric integration of accelerometer velocity data to yield displacement data
    acc_disp = lambda a, b : integrate.simps(acc_vel_pts[a:b], time[a:b])
    acc_disp_pts = [acc_disp(0, k+1)*(9.81) for k, v in enumerate(acc_vel_pts)]
    # Set maximum limit on the numeric integration time
    max_int_time = 2 # seconds
    # Collect the integral
    for i_t in range(c_points):
        if time[i_t] > max_int_time:
            acc_disp_pts[i_t] = 0

    # Gather damping coefficient information
    damp = damping(pp_times, pp_data, trial_mass)

    # Method 2: Potentiometer derived spring force
    pot_sp_f = np.array([((m_g - damp*pot_vel[i] - trial_mass*pot_accel[i]))/(2*(9.81**2))+m_g  for i in range(len(d_x))])
    # Method 4: Accelerometer derived spring force
    acc_sp_f = np.array([(m_g + damp*acc_vel_pts[i] + trial_mass*d_a[i]) for i in range(len(d_a))])
    # Method 1: Solve the ODE
    id_x, id_y = mass_spring(trial_mass, damp, s_const_k*1000, pp_data[0])
    # Shift y-values up to the baseline
    ode_y = [(i)*s_const_k + m_g for i in id_y]
    ode_x = [i + pp_times[0]+.1 for i in id_x]
    comp_lc_st = '--'
    compcol = 'C7'
    n_fig = 1

    # Group Photo: Clusterfuck
    plt.plot(ode_x, ode_y, label='ODE Integration (Method 1)',c='C0')
    plt.plot(time, pot_sp_f, label='Potentiometer Differentiation (Method2)', c='C1')
    plt.plot(time, m3_f_data, label='Spring Constant and Displacement (Method 3)', c='C2')
    plt.plot(time, acc_sp_f, label='Accelerometer Integration (Method 4)', c='C3')
    plt.plot(time, f_y, label='Force From Load Cell (Direct Measurement)', c='k', ls=':')
    plt.title('Figure {}: Force Calculation Method Comparison'.format(n_fig))
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.legend()
    # plt.savefig('Lab_10_figure_{}.png'.format(n_fig), bbox_inches='tight')
    n_fig +=1
    plt.show()

    # # Load Cell Calibration from static tests
    # plt.scatter(force_cal, f_cal_val, label='Mean Load Cell Reading')
    # plt.plot(force_cal, lcell_cal_list, color='r',ls='-.',label='Linear fit through origin')
    # plt.title('Figure {}: Load Cell Calibration'.format(n_fig))
    # plt.xlabel('Force Applied (Newtons)')
    # plt.ylabel('Load Cell Output')
    # plt.text(20,.06,'Load Cell Calibration Coefficient = {:1.2f}'.format(1/lcell_cal_coef))
    # plt.text(42.5,0,r'r$^2$ = ' + '{:1.4f}'.format(lc_rsq))
    # plt.legend()
    # plt.savefig('Lab_10_figure_{}.png'.format(n_fig), bbox_inches='tight')
    # n_fig +=1
    # plt.show()


    # # Spring Constant Derivation
    # plt.scatter(np.array(disp_cal), np.array(force_cal[1:]),label='Mean displacement with known mass')
    # plt.plot(cal_xaxis, cal_linfit_fcn_spring(cal_xaxis), color='r', ls='-.', label='Linear fit through origin')
    # plt.title('Figure {}: Spring Constant Calibration Data'.format(n_fig))
    # plt.xlabel('Displacement (mm)')
    # plt.ylabel('Force (N)')
    # plt.text(10.5,5.2,'Spring Constant = {:1.4f} N/mm'.format(s_const_k))
    # plt.text(16,2.5,r'r$^2$ = ' + '{:1.4f}'.format(sc_rsq))
    # plt.legend()
    # plt.savefig('Lab_10_figure_{}.png'.format(n_fig), bbox_inches='tight')
    # n_fig +=1
    # plt.show()

    # # Accelerometer Filtering
    # plt.plot(time, uf_d_a, label='Unfiltered Acceleration')
    # plt.plot(time, d_a, label='Filtered Acceleration')
    # plt.title('Figure {}: Accleration Data Filtering'.format(n_fig))
    # plt.xlabel('Time(s)')
    # plt.ylabel('Accelerometer Output')
    # plt.text(2.5,-11,'Butterworth Filter Parameters : ')
    # plt.text(2.5,-12,r'Order = 2, $f_s = 10000Hz, f_c = 20Hz$ ')
    # plt.legend()
    # plt.savefig('Lab_10_figure_{}.png'.format(n_fig), bbox_inches='tight')
    # n_fig +=1
    # plt.show()

    # # Accelerometer Integrated data
    # plt.plot(time, acc_disp_pts, label='Displacement')
    # plt.plot(time, acc_vel_pts, label='Velocity')
    # plt.plot(time, d_a, label='Acceleration')
    # plt.title('Figure {}: Accelerometer Data'.format(n_fig))
    # plt.xlabel('Time (s)')
    # plt.ylabel('Scaled Accelerometer Output')
    # plt.legend()
    # plt.savefig('Lab_10_figure_{}.png'.format(n_fig), bbox_inches='tight')
    # n_fig +=1
    # plt.show()


    # # Potentiometer (displacement) Filtering
    # plt.plot(time, uf_d_x, label='Unfiltered Displacement')
    # plt.plot(time, d_x, label='Filtered Displacement')
    # plt.scatter(pp_times, pp_data, label='Peak Detection Data', c='r')
    # plt.text(.6,0,r'Damping Coefficient = B = $\frac{mg - kx - m\dot{y}}{m\ddot{y}} = - \frac{2m * ln(\frac{y_2}{y_1})}{\Delta t}$ = ' + '{:1.2f}'.format(damp))
    # plt.text(2.5,45,'Butterworth Filter Parameters : ')
    # plt.text(2.5,42,r'Order = 2, $f_s = 10000Hz, f_c = 30Hz$ ')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Displacement (m)')
    # plt.title('Figure {}: Displacement Data Filtering'.format(n_fig))
    # plt.legend()
    # plt.savefig('Lab_10_figure_{}.png'.format(n_fig), bbox_inches='tight')
    # n_fig +=1
    # plt.show()

    # # Potentiometer derived data
    # plt.plot(time, d_x, label='Displacement')
    # plt.plot(time, [i/9.81 for i in pot_vel], label='Velocity')
    # plt.plot(time, [i/(9.81**2) for i in pot_accel], label='Acceleration')
    # plt.title('Figure {}: Potentiometer Data'.format(n_fig))
    # plt.xlabel('Time')
    # plt.ylabel('Scaled Potentiometer Output')
    # plt.legend()
    # plt.savefig('Lab_10_figure_{}.png'.format(n_fig), bbox_inches='tight')
    # n_fig +=1
    # plt.show()



    # # Method 1:
    # plt.plot(time, f_y, label='Load Cell Data',c='k', ls=comp_lc_st)
    # plt.plot(ode_x, ode_y, label='ODE Integration (Method 1)', c=compcol)
    # plt.title('Figure {}: Numeric ODE Solution'.format(n_fig))
    # plt.xlabel('Time (s)')
    # plt.ylabel('Force (N)')
    # plt.legend()
    # plt.savefig('Lab_10_figure_{}.png'.format(n_fig), bbox_inches='tight')
    # n_fig +=1
    # plt.show()

    # # Method 2:
    # plt.plot(time, f_y, label='Load Cell Data',c='k', ls=comp_lc_st)
    # plt.plot(time, pot_sp_f, label='Potentiometer Differentiation (Method2)', c=compcol)
    # plt.title('Figure {}: Potentiometer Derived Force'.format(n_fig))
    # plt.xlabel('Time (s)')
    # plt.ylabel('Force (N)')
    # plt.legend()
    # plt.savefig('Lab_10_figure_{}.png'.format(n_fig), bbox_inches='tight')
    # n_fig +=1
    # plt.show()

    # # Method 3:
    # plt.plot(time, f_y, label='Load Cell Data',c='k', ls=comp_lc_st)
    # plt.plot(time, m3_f_data, label='Spring Constant and displacement (Method 3)', c=compcol)
    # plt.title('Figure {}: Force from Spring Constant'.format(n_fig))
    # plt.xlabel('Time (s)')
    # plt.ylabel('Force (N)')
    # plt.legend()
    # plt.savefig('Lab_10_figure_{}.png'.format(n_fig), bbox_inches='tight')
    # n_fig +=1
    # plt.show()

    # # Method 4:
    # plt.plot(time, f_y, label='Load Cell Data',c='k', ls=comp_lc_st)
    # plt.plot(time, acc_sp_f, label='Accelerometer Integration (Method 4)', c=compcol)
    # plt.title('Figure {}: Accelerometer Derived Force Data'.format(n_fig))
    # plt.xlabel('Time (s)')
    # plt.ylabel('Force (N)')
    # plt.legend()
    # plt.savefig('Lab_10_figure_{}.png'.format(n_fig), bbox_inches='tight')
    # n_fig +=1
    # plt.show()

def lp_801_300(in_value):
    '''
    Returns displacement in mm from input voltage on Omega LP801-300 linear potentiometer
    '''
    in_value = abs(in_value)
    min_input = 0
    max_input = 3 # volts
    if in_value < min_input or in_value > max_input:
        print('''
        ERROR: Input value outside range for instrument : Potentiometer\n
        Minimum input value (volts) : {:1.2f} \t Maximum input value (volts) : {:1.2f}\n
        Input value received : {:1.2f}\n
        '''.format(min_input, max_input, in_value))
        exit()
    min_output = 304.8 # 12 inches to m
    max_output = 0
    output_data = (in_value * (max_output-min_output) / (max_input - min_input))
    # linearity = (max_input - min_input) * 0.01
    # hysteresis = 0.025 # mm
    # repeatability = 0.012 # mm
    # error = np.sqrt(linearity**2 + hysteresis**2 + repeatability**2)
    # print('LP801-300 Measurement Results:')
    # print('Measured Displacement : {:1.2f} mm'.format(output_data))
    # print('Uncertainty : +/- {:1.2f} mm'.format(error))
    return output_data

def adxl335(in_value):
    '''
    Returns acceleration from input voltage to Analog Devices ADXL335 Accelerometer
    '''
    min_input = 0
    max_input = 3 # Volts
    if in_value < min_input or in_value > max_input:
        print('''
        ERROR: Input value outside range for instrument : Accelerometer\n
        Minimum input value (volts) : {:1.2f} \t Maximum input value (volts) : {:1.2f}\n
        Input value received : {:1.2f}\n
        '''.format(min_input, max_input, in_value))
        exit()
    min_output = -3*9.80665
    max_output = 3*9.80665 # g's to m/s^2
    output_data = (in_value * (max_output-min_output) / (max_input - min_input))
    # linearity = (max_input - min_input) * 0.01
    # hysteresis = 0.025 # mm
    # repeatability = 0.012 # mm
    # error = np.sqrt(linearity**2 + hysteresis**2 + repeatability**2)
    # print('LP801-300 Measurement Results:')
    # print('Measured Displacement : {:1.2f} mm'.format(output_data))
    # print('Uncertainty : +/- {:1.2f} mm'.format(error))
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
    # Sum of the squares of residuals from the generated line
    s_sq_t = sum([((coef_a * x_list[i] + coef_b - y_list[i])**2) for i in range(n)])
    # Sum of the squares of residuals from the mean
    s_sq_r = sum([(y_list[i] - y_mean)**2 for i in range(n)])
    # Standard deviation
    # st_dev = (s_sq_r / (n-1))**(0.5)
    # R-Squared Value - coefficient of determination
    r_sq = 1 - (s_sq_t / s_sq_r)
    # Standard error
    # std_er = (s_sq_t/(n-2))**(0.5)
    # Find maximum error deviation from the best fit line
    # er_max = max([abs(coef_a * x_list[i] + coef_b - y_list[i]) for i in range(n)])
    print('Linear Best Fit: y = ( {:.4f} ) x {:+.4f}'.format(coef_a,coef_b))
    # print('Standard Deviation = {:.4f}'.format(st_dev))
    print('R-Squared, Calibration Constant = {:.4f}'.format(r_sq))
    # print('Standard Error = {:.4f}'.format(std_er))
    # print('Maximum Error = {:.4f}\n'.format(er_max))
    return coef_a, coef_b, r_sq

def lin_origin(x_list, y_list):
    '''
    Fits a line through the origin of the form y = a*x + 0 for instrument calibration
    applications.
    '''
    n_size = len(y_list)
    y_mean = sum(y_list)/n_size
    numer = 0
    denom = 0
    if n_size != len(x_list):
        print('Numerical Differentiation Error (lin_origin)\nSize of x-list and y-list must be the same\n')
        exit()
    for x_i in range(n_size):
        numer += x_list[x_i]*y_list[x_i]
        denom += x_list[x_i]**2
    coef_a = (numer/denom)
    s_sq_t = sum([((coef_a * x_list[i] - y_list[i])**2) for i in range(n_size)])
    s_sq_r = sum([(y_list[i] - y_mean)**2 for i in range(n_size)])
    r_sq = 1 - (s_sq_t / s_sq_r)

    return coef_a, r_sq

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
    centered finite difference with error = (O(h^2)) first two points and last two points are not valid.
    '''
    st_sz = abs(x_list[0] - x_list[1])
    n_size = len(y_list)
    # Check for dimension mismatch and data length
    if n_size != len(x_list):
        print('Numerical Differentiation Error (num_1deriv)\nSize of x-list and y-list must be the same\n')
        exit()
    # It needs at least 2 points to work
    elif n_size < 2:
        print('Numerical Differentiation Error (num_1deriv)\nData must be at least 2 values long.\n')
    # Preallocating the output list saves time in most languages, but doesn't really matter in python
    out_list = [None] * n_size
    # Runs through each case for the data points and returns the numerically derived derivative at the
    # given point for the whole list of data.
    for i_x in range(n_size):
        if i_x == 0:
            # First data point uses Forward Finite Divided Difference
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            f_deriv = (-p_2 + 4*p_1 -3*y_list[i_x]) / (2*st_sz)
        elif i_x == 1 or i_x == n_size-2:
            # The end points do not have as much data so the derivative loses accuracy, fewer series terms available
            p_1 = y_list[i_x + 1]
            m_1 = y_list[i_x - 1]
            f_deriv = (p_1 - m_1) / (2 * st_sz)
        elif i_x == (n_size - 1):
            # Last data point uses Backward Finite Divided Difference
            m_1 = y_list[i_x-1]
            m_2 = y_list[i_x-2]
            f_deriv = (3*y_list[i_x] - 4*m_1 + m_2) / (2*st_sz)
        else:
            # Centered method while the data exists
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            m_1 = y_list[i_x-1]
            m_2 = y_list[i_x-2]
            f_deriv = (-p_2 + 8*p_1 - 8*m_1 + m_2)/(12*st_sz)
        out_list[i_x] = f_deriv
    return out_list

def num_2deriv(x_list, y_list):
    '''
    Numerical Methods - Numeric Differentiation of a list of data points
    returns second derivative
    Forward Finite Divided difference at the start, Backward at the end, and centered in the middle
    Empirically, the error seems the worst at the second point and the second to last point with the
    more error prone centered divided difference formulas. potential future work may be to
    improve the error by using a more accurate forward or backward finite difference formula
    '''
    st_sz = abs(x_list[0] - x_list[1])
    n_size = len(y_list)
    if n_size != len(x_list):
        print('Numerical Differentiation Error (num_2deriv)\nSize of x-list and y-list must be the same\n')
        exit()
    elif n_size < 2:
        print('Numerical Differentiation Error (num_2deriv)\nData must be at least 2 values long.\n')
    # Preallocating the output list saves time in most languages, but doesn't really matter in python
    out_list = [None] * n_size
    # Runs through each case for the data points and returns the numerically derived derivative at the
    # given point for the whole list of data.
    for i_x in range(n_size):
        if i_x == 0:
            # First data point uses Forward Finite Divided Difference
            p_3 = y_list[i_x+3]
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            f_deriv = (-p_3 + 4*p_2 - 5*p_1 + 2*y_list[i_x])/(st_sz**2)
        elif i_x == 1 or i_x == n_size-2:
            # The end points do not have as much data so the derivative loses accuracy, fewer series terms available
            p_1 = y_list[i_x+1]
            m_1 = y_list[i_x-1]
            f_deriv = (p_1 - 2*y_list[i_x] + m_1)/(st_sz**2)
        elif i_x == n_size -1:
            # Last data point uses Backward Finite Divided Difference
            m_3 = y_list[i_x-3]
            m_2 = y_list[i_x-2]
            m_1 = y_list[i_x-1]
            f_deriv = (2*y_list[i_x] - 5*m_1 + 4*m_2 - m_3)/(st_sz**2)
        else:
            # Centered method while the data exists
            p_2 = y_list[i_x+2]
            p_1 = y_list[i_x+1]
            m_1 = y_list[i_x-1]
            m_2 = y_list[i_x-2]
            f_deriv = (-p_2 + 16*p_1 - 30*y_list[i_x] + 16*m_1 - m_2)/(12*st_sz**2)
        # Saves each point in its appropriate spot in the output list
        out_list[i_x] = f_deriv
    return out_list

def sim_int_num(x_list, y_list):
    '''
    Numerical Methods : Integration
    Numerically integrates an xy list using an optimized simpson algorithm.
    Requires equally spaced x-data.
    '''
    # Trapezoidal rule for 2 points
    trap = lambda h, f_0, f_1 : h * (f_0 - f_1) / 2
    # Simpsons 1/3 rule for 3 points
    simp_13 = lambda h, f_0, f_1, f_2 : 2*h*(f_0 + 4*f_1 + f_2)/6
    # Simpsons 3/8 rule for 4 points
    simp_38 = lambda h, f_0, f_1, f_2, f_3 : (3*h * (f_0 + 3* (f_1 + f_2) + f_3) / 8)
    st_sz = abs(x_list[0] - x_list[1])
    n_size = len(y_list)
    # Save the size of the dataset to handle even numbers
    m_size = n_size
    # Error checking on the data set for dimension mismatch
    if n_size != len(x_list):
        print('Numerical Integration Error (sim_int_num)\nSize of x-list and y-list must be the same\n')
        exit()
    # This function needs at least 2 points to run
    elif n_size < 2:
        print('Numerical Differentiation Error (sim_int_num)\nData must be at least 2 values long.\n')
    out_list = []
    # Trapezoidal rule gives the worst estimate of all of the methods in this function
    # but you gotta work with what you got.
    if n_size == 2:
        out_list.append(trap(st_sz, y_list[0], y_list[1]))
    # Simpson's 1/3 only works with odd numbers of data points. Using simpson's 3/8
    # on the last 4 points of the dataset and subtracting 3 points from the 1/3
    # iteration limit will handle this.
    elif (n_size % 2) == 0:
        f_0 = y_list[n_size-4]
        f_1 = y_list[n_size-3]
        f_2 = y_list[n_size-2]
        f_3 = y_list[n_size-1]
        out_list.append(simp_38(st_sz, f_0, f_1, f_2, f_3))
        m_size -= 3
    if m_size > 1:
        for i_x in range(0, m_size - 1, 2):
            f_0 = y_list[i_x]
            f_1 = y_list[i_x + 1]
            f_2 = y_list[i_x + 2]
            out_list.append(simp_13(st_sz, f_0, f_1, f_2))
    return sum(out_list)

def findpeaks(x_list, y_list, dy_list, d2y_list):
    '''
    Accepts lists of x values and y-values with numerically derived first and second derivatives
    returns list of indices for detected peaks. Requires filtered data.
    '''
    peak_points = []
    sign_toggle = 0
    n_pts = len(x_list)
    for x_i in range(n_pts):
        sign = sign_toggle
        if dy_list[x_i]*-1 > 0:
            # negative
            sign = 0
        else:
            sign = 1
        if sign != sign_toggle:
            sign_toggle = sign
            if d2y_list[x_i] < 0:
                peak_points.append(x_i)
    return peak_points

def damping(peaks_x, peaks_y, mass, skip=0):
    '''
    Determines damping coefficient from peak data
    skip number of detected peaks to get rid of collected points before the test
    '''
    offset = peaks_y[-1]
    x_1 = peaks_x[skip]
    y_1 = peaks_y[skip] - offset
    x_2 = peaks_x[skip+1]
    y_2 = peaks_y[skip+1] - offset
    dt = abs(x_2 - x_1)
    d_const_b = (-2 * mass * np.log(y_2/y_1))/dt
    # print('Damping Constant : {}'.format(d_const_b))
    return (d_const_b)

def mass_spring(mass, damp_coef, sp_const, i_disp):
    def dU_dx(U, x):
        grav = 9.81
        dU = U[1]
        d2U = (1/mass) * (mass*grav - (damp_coef*dU) - sp_const * U[0])
        return [dU, d2U]
    i_cond = [i_disp, 0]
    x_vals = np.linspace(0, 5, 1000)
    u_vals = integrate.odeint(dU_dx, i_cond, x_vals)
    y_vals = u_vals[:,0]
    return x_vals, y_vals

main()