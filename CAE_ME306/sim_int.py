## module sim_int
'''
Simpson's Numeric Integration method for both data points and known functions. Uses adaptive method for both odd and even numbers of points.
Points must be equally spaced.

See example21_6.py
'''

import numpy as np

def sim_int(fcn, l_bnd, u_bnd, n_point):
    '''
    Numerical Methods - Closed Numerical Integration

    Simpson's Rules

    Numerically integrates a function within lower and upper bounds over
    a given number of data points using second and third order Lagrange
    polynomials to approximate the function

    fcn : Function to integrate
    l_bnd : Lower bound on integration
    u_bnd : Upper bound on integration
    n_point : Number of data points to consider

    returns sum of the area below the curve of the function
    '''
    # Trapezoidal area
    trap = lambda h, f_0, f_1 : h * (f_0 - f_1) / 2
    def simp_38(h, f_0, f_1, f_2, f_3):
        '''
        Simpson's 3/8ths rule: Approximates a 3rd order Lagrange
        polynomial fit to four points.
        '''
        return (3*h * ((f_0 + 3* (f_1 + f_2) + f_3) / 8))
    def simp_13m(fcn, h, n):
        '''
        Simpson's 1/3rd rule: Multiple Application: Feed a function,
        height and number of points. Needs odd number of points
        '''
        simp13_sum = fcn(0)
        for i in range(2, n-1, 2):
            simp13_sum += (4 * fcn((i-1)*h)) + (2 * fcn(h*(i-2)))
        simp13_sum += (4 * fcn(h*(n-2)) + fcn(h*(n-1)))
        return (h * simp13_sum / (3))
    # Step height across the function
    height = (u_bnd - l_bnd)/(n_point-1)
    # Instantiate a variable to hold sum of the total integral
    st_int = 0
    # Check for application of trapezoid method
    if n_point == 1:
        st_int = trap(height, fcn(0), fcn(1))
    elif n_point > 1:
        # Stores a mutable version to hold number of points
        m_point = n_point
        # Determine if the number of points is odd
        if (n_point % 2) == 0:
            f_0 = fcn(height*(n_point - 4))
            f_1 = fcn(height*(n_point - 3))
            f_2 = fcn(height*(n_point - 2))
            f_3 = fcn(height*(n_point - 1))
            # The number of points is even, so use 3/8ths rule on the last 4 points
            st_int += simp_38(height, f_0, f_1, f_2, f_3)
            # Update the number of points to use 1/3rd rule on
            m_point -= 3
        if m_point > 1:
            # feed the rest of the points to Simpson's third
            st_int += simp_13m(fcn, height, m_point)
    return st_int

def sim_int_num(x_list, y_list):
    '''
    Numerical Methods : Integration
    Numerically integrates an xy list using an optimized simpson algorithm
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


