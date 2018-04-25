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

    tc_temp = lambda R, t : 503 + np.cos(2*np.pi*R*t)
    xvalues = np.linspace(0,0.01,10000)
    yvalues = tc_temp(800,xvalues)
    plt.plot(xvalues,yvalues)
    plt.xlabel('Time(s)')
    plt.ylabel('Thermocouple Reading (R)')
    plt.title('Thermocouple Time and Temp Data')
    plt.show()

main()
