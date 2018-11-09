## module div_dif_deriv
'''
Numerical Methods - Differentiation

Centered finite divided difference, 1st derivative:
cfdd_1deriv(fcn, val, step)
- Use when the function is known

Centered finite divided difference, 1st derivative for dataset:
num_1deriv(x_list, y_list)
- Use when calculating from a list of data points

Centered finite divided difference, 2nd derivative for dataset:
- num_2deriv(x_list, y_list)

see example4_4.py
'''
import numpy as np

def cfdd_1deriv(fcn, val, step):
    '''
    Numerical Methods : Numeric Differentiation

    Centered Finite Divided Difference - 1st Derivative

    Calculates the derivative of a function numerically

    fcn : Function to evaluate
    val : Value to evaluate the function at
    step : Step size for generating the estimation

    Returns derivative
    '''
    # Get two steps away
    t_step = 2*step
    # Function minus 2 steps
    fx_m2 = fcn(val - t_step)
    # Function minus 1 step
    fx_m1 = fcn(val - step)
    # Function plus 1 step
    fx_p1 = fcn(val + step)
    # Function plus 2 steps
    fx_p2 = fcn(val + t_step)
    # Run through Taylor series approximation
    return ((-fx_p2 + 8*fx_p1 - 8*fx_m1 + fx_m2)/(12*step))

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




