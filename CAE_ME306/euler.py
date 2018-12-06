## module euler
'''
Numerical Methods - Numeric Integration of ODE Initial Value Problems
def euler(func, x_0, x_f, y_0, n)
    Euler Method:

    Inputs:
    func : function with variables in the form of f(x,y)
    x_0, x_f : beginning and end points to evaluate the integral
    y_0 : Initial value for the dependent variable(s). Feed a 2-D numpy array to solve multiple equations.
    n : Number of intervals to use between x_0, x_f

    Outputs:
    x : List of independent variable values
    y : List of dependent variable values for each equation

    see example_euler_web.py
        prob25_1.py
'''
import numpy as np

def euler(func, x_0, x_f, y_0, n):
    '''
    Numerical Methods - Differential Equation Initial Value Problems

    ** Requires NUMPY import **
    import numpy as np

    Euler Method:

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
    x = np.linspace(x_0, x_f, n+1)
    # Generate a vector to hold y-values
    y = np.zeros([n+1])
    # Set the first initial value
    y[0] = y_0
    # Iterate through the calculation
    for i in range(1,n+1):
        # The next point is found by evaluating the function at this point
        y[i] = d_x*(func(x[i-1],y[i-1])) + y[i-1]
    # Return x and y vectors
    return x, y
