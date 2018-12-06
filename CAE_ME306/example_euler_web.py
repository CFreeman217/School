## module example_euler_web
''' Online test case for example running eulers method on a dataset for numeric integration estimation'''
import numpy as np
import matplotlib.pyplot as plt
from euler import euler

def online():
    x0 = 0
    y0 = 1
    xf = 10
    n = 100
    in_fun = lambda x,y : -y + np.sin(x)
    X, Y = euler(in_fun, x0, xf, y0, n)
    plt.plot(X, Y)
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.title('Approximate Solution with Forward Euler\'s Method')
    plt.show()

online()