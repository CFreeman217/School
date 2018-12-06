## module midpoint
'''
Numerical Methods - ODE Integration, Improved Euler's Method

Midpoint Method - First order Euler method where slope is determined from a point between the step
'''
import numpy as np

def midp_int(func, x_0, x_f, y_0, n):
    '''
    Numerical Methods - Differential Equation Initial Value Problems

    Midpoint Method:

    Inputs:
    func : function with variables in the form of f(x,y)
    x_0, x_f : beginning and end points to evaluate the integral
    y_0 : Initial value for the dependent variable(s). Feed a 2-D numpy array to solve multiple equations.
    n : Number of intervals to use between x_0, x_f

    Outputs:
    x : List of independent variable values
    y : List of dependent variable values for each equation
    '''
    # Determine the step size
    d_x = (x_f - x_0) / (n)
    # Create a vector of x-values
    X = np.linspace(x_0, x_f, n+1)
    # Generate a vector to hold y-values
    Y = np.zeros([n+1])
    # Set the first initial value
    Y[0] = y_0
    # Iterate through the calculation
    for i in range(1,n+1):
        k1 = func(X[i-1],Y[i-1])
        # The next point is found by evaluating the function at this point
        y_temp = Y[i-1] + d_x*(k1/2)
        k2 = func(X[i-1] + (d_x/2), y_temp)
        Y[i] = Y[i-1] + d_x*k2

    # Return x and y vectors
    return X, Y