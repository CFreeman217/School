## module prob25_26
'''
Demonstration of adaptive RK4/5 method on a system of 2nd order differential equations
'''
import numpy as np
import matplotlib.pyplot as plt
from runge_kutta5 import runge_kutta5

def prob25_26():
    def fcn(t, x):
        # Instantiate an array of zeros to hold the array elements
        fcn = np.zeros(6)
        # Mass of each jumper
        m1 = 60 # kg
        m2 = 70 # kg
        m3 = 80 # kg
        # Gravity
        g = 9.81 # m/s^2
        # Bungee Cord Spring Constant
        k1 = 50 # (N/m)
        k2 = 100 # (N/m)
        k3 = 50 # (N/m)
        # Velocities for each of the jumpers:
        # dx_1/dt = v1
        fcn[0] = x[3]
        # dx_2/dt = v2
        fcn[1] = x[4]
        # dx_3/dt = v3
        fcn[2] = x[5]
        # Displacements for each jumper:
        # dv_1/dt = g + (k2/m1)*x_2 - ((k1 + k2)/m1)*x_1
        fcn[3] = g + (k2/m1)*x[1] - ((k1 + k2)/m1)*x[0]
        # dv_2/dt = g + (k2/m2)*x_1 - ((k1 + k2)/m2)*x_2 + (k3/m2)*x_3
        fcn[4] = g + (k2/m2)*x[0] - ((k2 + k3)/m2)*x[1] + (k3/m2)*x[2]
        # dv_3/dt = g + (k3/m3)*x_2 - (k3/m3)*x_3
        fcn[5] = g + (k3/m3)*x[1] - (k3/m3) * x[2]
        return fcn
    # Start and ending times
    t0 = 0; tf = 100
    # Array holding the initial values (velocity and displacement) for each of the jumpers (everything starts at zero)
    x = np.array([0]*6)
    # Feed the data into the integrator
    X, Y = runge_kutta5(fcn, t0, tf, x)

    plt.plot(X, Y[:,0], label='m1 = 60kg')
    plt.plot(X, Y[:,1], label='m2 = 70kg')
    plt.plot(X, Y[:,2], label='m3 = 80kg')
    plt.xlabel('Time (s)')
    plt.ylabel('Displacement')
    plt.title('Bungee Jumper Displacement')
    plt.legend()
    plt.show()

    plt.plot(X, Y[:,3], label='m1 = 60kg')
    plt.plot(X, Y[:,4], label='m2 = 70kg')
    plt.plot(X, Y[:,5], label='m3 = 80kg')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Bungee Jumper Velocity')
    plt.legend()
    plt.show()
prob25_26()