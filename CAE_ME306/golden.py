## module golden
'''
Numerical Methods:
One-Dimensional Unconstrained Optimization:
Golden Section Search

Finds the maximum or minimum for an input function between two given points
using the golden ratio.

func : Input function to evaluate
x_low : Lower bound
x_high : Upper bound
er_max : Error threhsold (Optional, default is 0.0001)
it_max : Max iterations (Optional, default is 100)
maxima : When true, finds local maximum, when false, finds local minimum

Returns x value, y value, error
See prob13_6a.py
    prob13_18b.py
'''

def golden(func, x_lower, x_upper, er_max=0.0001, it_max=100, maxima=True):
    '''
    One-Dimensional Unconstrained Optimization:
    Golden Section Search

    Finds the maximum or minimum for an input function between two given points
    using the golden ratio.

    func : Input function to evaluate
    x_low : Lower bound
    x_high : Upper bound
    er_max : Error threhsold (Optional, default is 0.0001)
    it_max : Max iterations (Optional, default is 100)
    maxima : When true, finds local maximum, when false, finds local minimum

    Returns x value, y value, error
    '''
    # Set up golden ratio as a constant
    R = (5**(0.5)-1)/2
    # Store the initial values in variables that will change within the function
    x_low = x_lower
    x_high = x_upper
    # Current error
    c_error = 1
    # Find movement through the first iteration
    d = R*(x_high - x_low)
    # Generate low and high guesses for the new x values
    x_one = x_low + d
    x_two = x_high - d
    # Find the function output from these two guesses
    y_one = func(x_one)
    y_two = func(x_two)
    # Iterate within the limits of the maximum number of iterations
    for iter_num in range(it_max):
        # Check for convergence
        if c_error < er_max:
            print('Met error threshold after {} iterations.'.format(iter_num))
            break
        # If we are finding the maximum, and y_one is greater, or vice versa
        if ((y_one > y_two) and (maxima == True)) or ((y_one < y_two) and (maxima == False)):
            # Store the low value in
            x_low = x_two
            x_two = x_one
            x_one = x_low + R * (x_high - x_low)
            y_one = func(x_one)
            y_two = func(x_two)
            c_error = (1 - R) * abs((x_high - x_low) / x_one)
        else:
            x_high = x_one
            x_one = x_two
            x_two = x_high - R * (x_high - x_low)
            y_one = func(x_one)
            y_two = func(x_two)
            c_error = (1 - R) * abs((x_high - x_low)/x_two)
        if ((y_one > y_two) and (maxima == True)) or ((y_one < y_two) and (maxima == False)):
            x_opt = x_one
        else:
            x_opt = x_two
    return x_opt, func(x_opt), c_error

