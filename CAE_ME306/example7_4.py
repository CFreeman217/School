## module example7_4
'''
Demonstration of 4th order Runge-Kutta method with fixed step size
'''
import numpy as np
import matplotlib.pyplot as plt
from runge_kutta4 import runge_kutta4
def ex7_4():
    def fcn(x, y):
        fcn = np.zeros(2)
        fcn[0] = y[1]
        fcn[1] = -0.1*y[1] - x
        return fcn
    x0 = 0
    xf = 2
    y = np.array([0.0, 1.0])
    h = 0.2
    X, Y = runge_kutta4(fcn, x0, xf, y, n=0, st_sz=h)
    yExact = 100.0*X - 5.0*X**2 + 990.0*(np.exp(-0.1*X) - 1.0)
    plt.scatter(X,Y[:,0],label='RK4 Method')
    plt.plot(X,yExact,label='Exact Solution')
    plt.xlabel('X-Values')
    plt.ylabel('Y-Values')
    plt.title('4th-Order Runge-Kutta Example')
    plt.legend()
    plt.show()

ex7_4()