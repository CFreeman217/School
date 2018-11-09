## module example7_8
'''Test case for 5th order runge kutta adaptive algorithm for numeric ODE integration of moderately stiff systems'''
import numpy as np
from printSoln import printSoln
from runge_kutta5 import runge_kutta5

def ex7_8():

    '''
    The aerodynamic drag force acting on a certain object in free fall can be aproximated by:

    F_d = a * v^2 * e^(-b * y)

    Where:
    v = velocity (m/s)
    y = elevation (m)
    a = drag coefficient = 7.45 (kg/m)
    b = exponent thing = 10.53e-5 (m^-1)

    The differential equation describing the fall is:

    my'' = -mg * F_d

    Where
    g = 9.80665 m/s^2
    m = 114 kg

    If the object is released from an elevation of 9 km, determine the elevation and speed after 10 seconds free fall with the adaptive RK method.
    '''
    '''
    1.) Solve for y'' = -g + (a/m) * y'^2 * e^(-by) = -9.80665 + (7.45/114) * y'^2 * e^(-10.53e-5 * y)
        y(0) = 9000 m , y'(0) = 0

    y' = [y'_0] = [                         y_1                        ]
         [y'_1]   [ -9.80665 + (7.45/114) * y_1^2 * e^(-10.53e-5 * y_0)]

    y(0) = [ 9000m ]
           [   0   ]
    '''
    def fcn(x,y):
        fcn = np.zeros(2)
        fcn[0] = y[1]
        fcn[1] = -9.80665 + (7.45/114) * y[1]**2 * np.exp(-10.53e-5 * y[0])
        return fcn

    x0 = 0
    xf = 10
    y0 = np.array([9000,0.0])
    h = 0.5
    freq = 1
    X, Y = runge_kutta5(fcn, x0, xf, y0, h, 1.0e-2)
    printSoln(X, Y, freq)

ex7_8()