from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 2.0  # length of pendulum 2 in m
M1 = 2.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg

def springy_angles():
    '''
    Mass M1 is connected to a rigid, lightweight lever. assume that L1 = L2 = 0.25m,
    M1 = 2kg, K1 = 200_N/m. Negligible friction in the pivot. The input is
    displacement x. When x and theta are zero, the springs are at their free lengh.
    Assuming theta is small, derive the equation of motion for theta with x as
    the input. From the equation of motion, determine the systems natural frequency.
    '''
    G = 9.8  # gravity m/s^2
    L1 = 0.25 # length 1 m
    L2 = 0.25 # length 2 m
    L3 = 0.75 # length 3 m
    M1 = 2  # mass 1
    K1 = 100 # N/m
    K2 = 200 # N/m
    X1_0 = 0.2 # Initial value for x1 displacement
    V1_0 = 0.0
    t1_0 = 0.0 # Initial angle
    w1_0 = 0.0 # Initial angular velocity
    # Create an initial value array from the inputs above
    i_in = np.array([X1_0, t1_0, w1_0])
    # Function to hold the state variables. In MATLAB this is done in a separate m-file.
    def bobblebar(i_in, t):
        # Initialize the return variable
        dydx = np.zeros(3)
        print(i_in)
        dydx[0] = i_in[2]
        dydx[1] = (- K1*i_in[1]*(L1**2) - K2*(i_in[0] - L2*i_in[1])*L2 - M1*G*i_in[1]*L3) / (M1*(L3**2))
        dydx[2] = i_in[0]

        return dydx
    # Create a time array to hold the start and end times. The ODE routine will handle the time steps as it needs
    dt = 0.05
    t = np.arange(0.0, 2, dt)

    y = integrate.odeint(bobblebar, i_in, t)
    # Collect the position of each of the two masses over the time interval from the angular displacement information
    plt.plot(t,y[:,0], label='Something')
    plt.legend()
    plt.show()
    plt.plot(t,y[:,1], label='Something Else')
    plt.legend()
    plt.show()
    plt.plot(t,y[:,2], label='Nothing')
    plt.legend()
    plt.show()
    # # X-Displacement is the length of the bar * sin of the displacement angle
    # x1 = L1*sin(Y[:,0])
    # # Use negative here because the anchor point is above the position of the masses at the equilibrium position
    # y1 = -L1*cos(Y[:,0])
    # # Mass 2 is stuck at the end of arm L1, so we need to add those coordinates onto the end of the position output
    # x2 = L2*sin(Y[:,2]) + x1
    # y2 = -L2*cos(Y[:,2]) + y1

springy_angles()
# def derivs(state, t):

#     dydx = np.zeros_like(state)
#     dydx[0] = state[1]

#     del_ = state[2] - state[0]
#     den1 = (M1 + M2)*L1 - M2*L1*cos(del_)*cos(del_)
#     dydx[1] = (M2*L1*state[1]*state[1]*sin(del_)*cos(del_) +
#                M2*G*sin(state[2])*cos(del_) +
#                M2*L2*state[3]*state[3]*sin(del_) -
#                (M1 + M2)*G*sin(state[0]))/den1

#     dydx[2] = state[3]

#     den2 = (L2/L1)*den1
#     dydx[3] = (-M2*L2*state[3]*state[3]*sin(del_)*cos(del_) +
#                (M1 + M2)*G*sin(state[0])*cos(del_) -
#                (M1 + M2)*L1*state[1]*state[1]*sin(del_) -
#                (M1 + M2)*G*sin(state[2]))/den2

#     return dydx

# # create a time array from 0..100 sampled at 0.05 second steps


# # th1 and th2 are the initial angles (degrees)
# # w10 and w20 are the initial angular velocities (degrees per second)
# th1 = np.pi
# w1 = 0.0
# th2 = np.pi
# w2 = 0.0
# # th1 = 0.1
# # w1 = 0.0
# # th2 = 0.17
# # w2 = 0.0
# # initial state
# state = np.array([th1, w1, th2, w2])

# # integrate your ODE using scipy.integrate.

# x1 = L1*sin(y[:, 0])
# y1 = -L1*cos(y[:, 0])

# x2 = L2*sin(y[:, 2]) + x1
# y2 = -L2*cos(y[:, 2]) + y1

# # plt.plot(t,y[:, 0], t,y[:, 2])
# # plt.show()
# fig = plt.figure()
# ax = fig.add_subplot(111, autoscale_on=False, xlim=(-3.5, 3.5), ylim=(-3.5, 3.5))
# ax.grid()

# line, = ax.plot([], [], 'o-', lw=2)
# time_template = 'time = %.1fs'
# time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

# def init():
#     line.set_data([], [])
#     time_text.set_text('')
#     return line, time_text

# def animate(i):
#     thisx = [0, x1[i], x2[i]]
#     thisy = [0, y1[i], y2[i]]

#     line.set_data(thisx, thisy)
#     time_text.set_text(time_template % (i*dt))
#     return line, time_text

# ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
#                               interval=25, blit=True, init_func=init)

# # ani.save('double_pendulum_partA.mp4', fps=15)
# plt.show()