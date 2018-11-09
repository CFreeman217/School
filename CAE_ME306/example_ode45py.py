'''
Example of a python imitation of the popular MATLAB ordinary differential equation solver ode45.
'''
import numpy as np
import matplotlib.pyplot as plt
from NumericalMethods import ode45py

def example_ode45py():
    '''
    Three linked bungee jumpers are depicted in figure P25.26.
    If the bungee cords are adealized as linear springs,
    the following equations based on force balances can be developed:

    m_1 * d2x/dt2 = m_1*g + k2*(x_2 - x_1) - k1*x_1
    m_2 * d2x/dt2 = m_2*g + k3*(x_3 - x_2) - k2*(x_1 - x_2)
    m_3 * d2x/dt2 = m_3*g + k3*(x_2 - x_3)

    Where:
    m_i = mass of jumper i (kg)
    kj = spring constant for bungee cord j (N/m)
    x_i = displacement of jumper i starting from the top of the fall and positive downward (m)
    g = gravity = 9.81 m/s^2

    Solve these equations for the positions and velocities of the three
    jumpers given the initial conditions that all positions and velocities are zero at t=0.
    Use the following parameters for your calculations:

    m_1 = 60 kg
    m_2 = 70 kg
    m_3 = 80 kg
    k1 = k3 = 50 N/m
    k2 = 100 N/m
    '''
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
    # Array for start and ending times
    t = np.array([0, 100])
    # Array holding the initial values (velocity and displacement) for each of the jumpers (everything starts at zero)
    x = np.array([0]*6)
    # Feed ode45py almost exactly like you would in MATLAB
    X, Y = ode45py(fcn, t, x, iter_lim=200000)

    # Displacement data is stored in the first three columns
    plt.plot(X, Y[:,0], label='m1 = 60kg')
    plt.plot(X, Y[:,1], label='m2 = 70kg')
    plt.plot(X, Y[:,2], label='m3 = 80kg')
    plt.xlabel('Time (s)')
    plt.ylabel('Displacement (m)')
    plt.title('Bungee Jumper Displacement')
    plt.legend()
    plt.show()

    # Velocity data is stored in the last three columns
    plt.plot(X, Y[:,3], label='m1 = 60kg')
    plt.plot(X, Y[:,4], label='m2 = 70kg')
    plt.plot(X, Y[:,5], label='m3 = 80kg')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Bungee Jumper Velocity')
    plt.legend()
    plt.show()
example_ode45py()