## module prob25_18
'''
Demonstration of adaptive RK4/5 method on 2nd order differential equation
d2x/dt2 + (5x) * dx/dt + (x+7)sin(wt) = 0
w = 1
x'(0) = 1.5
x(0) = 6
t_0 = 0
t_f = 15
'''
import numpy as np
import matplotlib.pyplot as plt
from runge_kutta5 import runge_kutta5

def prob25_18():
    def fcn(t, x):
        w = 1
        # Instantiate zeros to hold function outputs
        fcn = np.zeros(2)
        # z = y'
        fcn[0] = x[1]
        # dz/dt = -0.6*y' - 8*y
        fcn[1] = (-5*x[0])*(x[1]) - (x[0] + 7) * np.sin(w * t)
        return fcn
    t0 = 0
    tf = 15
    # x = ( x(0) , x'(0) )
    x = np.array([6, 1.5])

    X, Y = runge_kutta5(fcn, t0, tf, x)

    plt.plot(X, Y[:,0], label='x_1')
    plt.plot(X, Y[:,1], label='x_2')
    plt.xlabel('X - Values')
    plt.ylabel('Y - Values')
    plt.title('Adaptive Runge-Kutta vs. 2nd Order ODE')
    plt.legend()
    plt.show()
prob25_18()