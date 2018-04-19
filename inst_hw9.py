import numpy as np
import matplotlib.pyplot as plt

def prob3():
    # Time constant determination from time and temp data
    # tau = reciiprocal of slope for regression line for:
    #           ln[(t - t_m) / (t_0 - t_m)]
    out_temp = 0 # Celsius
    ref_temp = 24 # Celsius
    time = [0.1, 0.5, 1.0, 2.0, 3.0]
    temp = [16.4, 8.3, 2.9, 0.7, 0.1]
    t_const = lambda x : np.log((x - out_temp)/(ref_temp - out_temp))
    tau_data = [t_const(i) for i in temp]
    a, b, r = lin_reg(time, tau_data)
    time_c = -1/a
    print('Time Constant = {:1.2f}'.format(time_c))


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
    st_dev = (s_sq_r / (n-1))**(0.5)
    # R-Squared Value - coefficient of determination
    r_sq = 1 - (s_sq_t / s_sq_r)
    print('Linear Best Fit: y = ( {:.4f} ) x {:+.4f}'.format(coef_a,coef_b))
    print('Standard Deviation = {:.4f}'.format(st_dev))
    print('R-Squared, Calibration Constant = {:.4f}'.format(r_sq))
    return coef_a, coef_b, r_sq

prob3()