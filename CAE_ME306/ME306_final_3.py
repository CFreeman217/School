from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
from NumericalMethods import ode45py

def me306_final_3():
    G = 9.8  # gravity m/s^2
    L1 = 1  # length pendulum 1 m
    L2 = 2  # length pendulum 2 m
    M1 = 2  # mass pendulum 1 kg
    M2 = 1  # mass pendulum 2 kg
    # t1_0 = 0.1 # Initial value for theta 1 displacement
    # w1_0 = 0 # Initial value for angular velocity
    # t2_0 = 0.17 # Initial value for theta 2 displacement
    # w2_0 = 0 # Initial value for angular velocity
    # fig_name = '3a'
    t1_0 = np.pi # Initial value for theta 1 displacement
    w1_0 = 0 # Initial value for angular velocity
    t2_0 = np.pi # Initial value for theta 2 displacement
    w2_0 = 0 # Initial value for angular velocity
    fig_name = '3b'
    # Create an initial value array from the inputs above
    i_theta = np.array([t1_0, w1_0, t2_0, w2_0])
    # Function to hold the state variables. In MATLAB this is done in a separate m-file.
    def double_pend(t, theta):
        # Initialize the return variable
        dydx = np.zeros(4)
        # Place the velocities in to the state vector
        dydx[0] = theta[1]
        dydx[2] = theta[3]
        # Delta theta is equal to theta 2 minus theta 1
        d_0 = theta[2] - theta[0]
        # Letter substitutions for handling the coefficients to the derivatives
        sA = (M1+M2)*L1
        sB = M2*L2*cos(d_0)
        sC = M2*L1*cos(d_0)
        sD = M2*L2
        sE = -M2*L2*(theta[3]**2)*sin(d_0) - G*(M1+M2)*sin(theta[0])
        sF = M2*L1*(theta[1]**2)*sin(d_0) - G*M2*sin(theta[2])
        # Set your second derivatives into the state vector
        dydx[1] = (sF*sB - sD*sE) / (sB*sC - sD*sA)
        dydx[3] = (sE*sC - sA*sF) / (sB*sC - sD*sA)
        return dydx
    # Create a time array to hold the start and end times. The ODE routine will handle the time steps as it needs
    d_time = np.array([0,100])
    # Call my home brew ODE45 routine much like you would in MATLAB
    X, Y = ode45py(double_pend, d_time, i_theta)
    # Collect the position of each of the two masses over the time interval from the angular displacement information
    # X-Displacement is the length of the bar * sin of the displacement angle
    x1 = L1*sin(Y[:,0])
    # Use negative here because the anchor point is above the position of the masses at the equilibrium position
    y1 = -L1*cos(Y[:,0])
    # Mass 2 is stuck at the end of arm L1, so we need to add those coordinates onto the end of the position output
    x2 = L2*sin(Y[:,2]) + x1
    y2 = -L2*cos(Y[:,2]) + y1

    # Plot the angular displacements
    plt.plot(X,Y[:,0],label=r'$\Theta_1$')
    plt.plot(X,Y[:,2],label=r'$\Theta_2$')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (radians)')
    plt.title(fig_name + ' Angular Displacement')
    plt.legend()
    plt.savefig('ME306_prob_{}_disp.png'.format(fig_name),bbox_inches='tight')
    plt.show()

    # Plot the trajectory for each mass
    plt.plot(x2,y2,label=r'$m_2$',c='C1')
    plt.plot(x1,y1,label=r'$m_1$',c='C0')
    plt.xlabel('X - Axis (Horizontal)')
    plt.ylabel('Y - Axis (Vertical)')
    plt.title(fig_name + ' Mass Trajectory')
    plt.legend()
    plt.savefig('ME306_prob_{}_traj.png'.format(fig_name),bbox_inches='tight')
    plt.show()

me306_final_3()