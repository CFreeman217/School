import math
import numpy as np
def xexp_reg(x_data, y_data):
    '''
    Numerical Methods : Exponential curve fit
    Input x and y data points,

    Returns exponential curve fit constants A and b
    y = Ax * exp(b*x)
    '''
    # Get the size of the dataset
    size = len(x_data)
    # To get the desired regression equation result, we take the natural log of y_i/x_i
    ln_y = [math.log(y_data[i]/x_data[i]) for i in range(size)]

    # X_hat and Z_hat comes from using weighted averages for the data to generate a better fit
    x_hat_num = sum([(y_data[i]**2)*x_data[i] for i in range(size)])
    z_hat_num = sum([(y_data[i]**2)*ln_y[i] for i in range(size)])
    # Sum of y_data square
    sy_sq = sum([y_data[i]**2 for i in range(size)])
    # New coefficients for linear fit
    x_hat = x_hat_num / sy_sq
    z_hat = z_hat_num / sy_sq
    # Generate the b-parameter
    coef_b_num = sum([(y_data[i]**2) * ln_y[i] * (x_data[i] - x_hat) for i in range(size)])
    coef_b_den = sum([(y_data[i]**2) * x_data[i] * (x_data[i] - x_hat) for i in range(size)])
    coef_b = coef_b_num / coef_b_den
    # Find the A coefficient
    coef_A = np.exp(z_hat - coef_b * x_hat)
    # Set up the function to calculate residuals and give feedback on how the curve fits the data
    func = lambda x : x * coef_A * np.exp(coef_b * x)
    # Sum of the residuals from the calculation
    s_resi = sum([(y_data[i] - func(x_data[i]))**2 for i in range(size)])
    # Standard deviaton from the data. Small numbers are good here
    std_dev = (s_resi / (size - 2))**(0.5)
    # print('Exponential Curve Fit Standard Deviation : {}'.format(std_dev))
    return coef_A, coef_b, std_dev