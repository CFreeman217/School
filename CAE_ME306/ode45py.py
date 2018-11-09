#! /usr/bin/env python3
## module ode45py
'''
Numerical Methods - Moderately stiff numeric ODE solvers

4th order - 5th order Runge-Kutta algorithm with adaptive step size
Uses Dormand-Prince coefficient matrix for adjusting weighting on the algorithm
This solver mimics MATLAB's ODE45 function.

ode45py(func, x, y, st_sz=1.0e-4, tol=1.0e-5)

    Input:
    func : Function to evaluate in the form F(x,y)
    x : x-vector containing initial and final values to evaluate the integral
    y : y-vector with functions to evaluate
    st_sz : Step size to run across the integral for initial estimate
    tol : Error estimate tolerance for determining whether to adjust step size

    Output:
    X : x-vector as numpy array
    Y : y-vector as numpy array

    See example_ode45py.py
'''
import numpy as np

def ode45py(func, x, y, st_sz=1.0e-4, tol=1.0e-5):
    '''
    Numerical Methods: Differential Equations, Initial Value Problems

    4th-order / 5th-order Runge-Kutta Method
    Includes adaptive step size adjustment
    Imitates MATLAB ode45 functionality and output
    '''
    # Dormand-Prince coefficients for RK algorithm -
    # Basically some people much smarter than me found the best numbers to fit in the weights for each
    # component of the calculation. These numbers determine how a solving algorithm will respond to a given problem.
    # This is the reason this particular solver yields a similar output to the matlab function of the same name.
    a1 = 0.2; a2 = 0.3; a3 = 0.8; a4 = 8/9; a5 = 1.0; a6 = 1.0
    c0 = 35/384; c2 = 500/1113; c3 = 125/192; c4 = -2187/6784; c5=11/84
    d0 = 5179/57600; d2 = 7571/16695; d3 = 393/640; d4 = -92097/339200; d5 = 187/2100; d6 = 1/40
    b10 = 0.2
    b20 = 0.075; b21 = 0.225
    b30 = 44/45; b31 = -56/15; b32 = 32/9
    b40 = 19372/6561; b41 = -25360/2187; b42 = 64448/6561; b43 = -212/729
    b50 = 9017/3168; b51 = -355/33; b52 = 46732/5247; b53 = 49/176; b54 = -5103/18656
    b60 = 35/384; b62 = 500/1113; b63 = 125/192; b64 = -2187/6784; b65 = 11/84
    # Store initial values
    x_f = x[1]
    x_n = x[0]
    y_n = y
    # Initialize variables
    X = []
    Y = []
    # Add the first set of known conditions
    X.append(x_n)
    Y.append(y_n)
    # Set up to break the for loop at the end
    stopper = 0 # Integration stopper, 0 = off, 1 = on
    # Initialize a k0 to start with the step size
    k0 = st_sz * func(x_n, y_n)
    # Generate the RK coefficients
    for _ in range(500):
        k1 = st_sz * func(x_n + a1*st_sz, y_n + b10*k0)
        k2 = st_sz * func(x_n + a2*st_sz, y_n + b20*k0 + b21*k1)
        k3 = st_sz * func(x_n + a3*st_sz, y_n + b30*k0 + b31*k1 + b32*k2)
        k4 = st_sz * func(x_n + a4*st_sz, y_n + b40*k0 + b41*k1 + b42*k2 + b43*k3)
        k5 = st_sz * func(x_n + a5*st_sz, y_n + b50*k0 + b51*k1 + b52*k2 + b53*k3 + b54*k4)
        k6 = st_sz * func(x_n + a6*st_sz, y_n + b60*k0 + b62*k2 + b63*k3 + b64*k4 + b65*k5)
        # Getting to the slope is the whole point of this mess
        dy = c0*k0 + c2*k2 + c3*k3 + c4*k4 + c5*k5
        # Determine the estimated change in slope by comparing the output coefficients for each RK coefficient
        E = (c0 - d0)*k0 + (c2 - d2)*k2 + (c3 - d3)*k3 + (c4 - d4)*k4 + (c5 - d5)*k5 - d6*k6
        # Find the estimated error using a sum of squares method
        e = np.sqrt(np.sum(E**2)/len(y_n))
        # we don't know if the new value i
        hNext = 0.9*st_sz*(tol/e)**0.2
        # If approximated error is within tolerance, accept this integration step and move on
        if e <= tol:
            # Store the new result
            y_n = y_n + dy
            # Increment the x-value by the new step size
            x_n = x_n + st_sz
            # Add the new values into the output vector
            X.append(x_n)
            Y.append(y_n)
            # Check to break the loop when we have reached the desired x-value
            if stopper == 1: break # Reached end of x-range
            # Set limits on how much the next step size can increase to avoid missing data points
            if abs(hNext) > 10.0*abs(st_sz):
                hNext = 10.0*st_sz
            # Determine if the algorithm has reached the end of the dataset
            if (st_sz > 0.0) == ((x_n + hNext) >= x_f):
                hNext = x_f - x_n
                # Sets the break condition for the next loop iteration
                stopper = 1
            # Setting k0 to k6 * (next step size) / (current step size) forces the algorithm to use the 4th order formula for the next step
            k0 = k6*hNext/st_sz
        else:
            # The error estimate is outside the required threshold to move on, we need to redo the calculation with a smaller step size
            if abs(hNext) < 0.1*abs(st_sz):
                # This cuts the step size into 1/10th the original size
                hNext = 0.1*st_sz
            # Set up k0 to go through the 5th order RK method on the next iteration because the error was no good.
            k0 = k0*hNext/st_sz
        # Set the next iteration step size
        st_sz = hNext
    # Returns the arrays for x and y values
    return np.array(X), np.array(Y)
