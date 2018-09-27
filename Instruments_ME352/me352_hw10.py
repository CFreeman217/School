import numpy as np
import matplotlib.pyplot as plt

def main():
    '''
    Problem 1:
    Air is heated in an automotive engine block (inside the cylinder).
    The cyclic measured temperature (from the thermocouple) can be
    approximated with:

    T_tc(t) = 503 + 49 cos (2 * pi * R * t)

    where:
    R = RPM (800 is standard 4-cyl.)
    tau = 0.41 seconds

    Calculate the average, maxmimum, and minimum measured temperature.
    Estimate the actual air temperature as a function of time.
    '''
    K_ss = 1 # Static sensitivity constant
    tau = 0.41 # Time constant, seconds
    w_0 = 2*np.pi # omega
    tc_temp = lambda R, t : 503 + np.cos(2*np.pi*R*t)
    phi = -np.arctan(w_0*tau) # Phase angle shift
    xvalues = np.linspace(0,0.1,500)
    yvalues = tc_temp((800),xvalues)
    max_t = max(yvalues)
    min_t = min(yvalues)
    amp = (max_t - min_t)/2
    t_av = (min_t + max_t)/2
    x_0 = (amp*(1+(w_0**2)*(tau**2))**(0.5))/K_ss
    t_actual = lambda t : t_av + x_0 * np.sin(w_0 * t + phi)

    plt.plot(xvalues,yvalues, label='Thermocouple Reading')
    plt.plot(xvalues,t_actual(xvalues), label='Actual Temperature estimate')
    plt.xlabel('Time(s)')
    plt.ylabel('Thermocouple Reading (R)')
    plt.title('Thermocouple Time and Temp Data')
    plt.legend()
    plt.show()

main()
