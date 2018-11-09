## module prob25_1
'''Problem 25_1 test case for euler's method'''
import numpy as np
import matplotlib.pyplot as plt
from euler import euler
from midpoint import midp_int
from runge_kutta4 import runge_kutta4

def prob25_1():
    # Input function
    in_fun = lambda t, y : y*(t**2) - 1.1*y
    t = np.linspace(0,2,100)
    y_anal = np.exp((t**3)/3 - 1.1*t)
    # Initial values
    x1_0 = 0
    x1_f = 2
    y1_0 = 1
    n1_s = 4
    n2_s = 8
    # Run the function
    X1, Y1 = euler(in_fun, x1_0, x1_f, y1_0, n1_s)
    X2, Y2 = euler(in_fun, x1_0, x1_f, y1_0, n2_s)
    X3, Y3 = midp_int(in_fun, x1_0, x1_f, y1_0, n1_s)
    X4, Y4 = runge_kutta4(in_fun, x1_0, x1_f, y1_0, n1_s)
    # plot
    plt.plot(t, y_anal, label='Analytical Soln.')
    plt.plot(X1, Y1, label='Euler h=0.5')
    plt.plot(X2, Y2, label='Euler h=0.25')
    plt.plot(X3, Y3, label='Midpoint h=0.5')
    plt.plot(X4, Y4, label='RK4 h=0.5')
    plt.xlabel('X - Values')
    plt.ylabel('Y - Values')
    plt.title('Integration Method and Step Size Comparison')
    plt.legend()
    plt.show()
prob25_1()