## module prob25_4
'''
Demonstration of 4th order RK method on 2nd order ODE

d2y/dx2 + 0.6*(dy/dx) + 8*y = 0

y(0) = 4
y'(0) = 0
Solve from x = 0 to x = 5
h = 0.5

'''
import numpy as np
import matplotlib.pyplot as plt
from runge_kutta4 import runge_kutta4

def prob25_4():
    def fcn(x, y):
        # Instantiate zeros to hold function outputs
        fcn = np.zeros(2)
        # z = y'
        fcn[0] = y[1]
        # dz/dt = -0.6*y' - 8*y
        fcn[1] = -0.6*y[1] - 8*y[0]
        return fcn
    x0 = 0
    xf = 5
    # y = ( y(0) , y'(0) )
    y = np.array([4, 0])
    h = 0.5
    X, Y = runge_kutta4(fcn, x0, xf, y, st_sz=h)

    plt.plot(X, Y[:,0], label='y_1')
    plt.plot(X, Y[:,1], label='y_2')
    plt.xlabel('X - Values')
    plt.ylabel('Y - Values')
    plt.title('Runge-Kutta vs. 2nd Order ODE')
    plt.legend()
    plt.show()
prob25_4()