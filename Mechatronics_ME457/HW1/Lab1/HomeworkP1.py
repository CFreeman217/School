import os, numpy as np, matplotlib.pyplot as plt

trap = lambda h, f_0, f_1 : h * (f_0 - f_1) / 2

def main():
    if 'weds_pm_Feb_04_04_19-0.csv' in os.listdir('.'):
        millis, ax, ay = np.loadtxt(open('weds_pm_Feb_04_04_19-0.csv'),
                                        delimiter=',',
                                        skiprows=1,
                                        unpack=True,
                                        usecols=(1,2,3))
        # vx = sim_int_num(millis, ax)

        # vy = sim_int_num(millis, ay)

    vx = []
    vy = []
    for key, val in enumerate(millis):
        if key == 0:
            # next
            dt = millis[1]
        else:
            dt = millis[key] - millis[key-1]
        vx.append(trap(dt, ax[key-1], ax[key]))
        vy.append(trap(dt, ay[key-1], ay[key]))

    plt.plot(millis, vx, label='X-Velocity')
    plt.plot(millis, vy, label='Y-Velocity')
    plt.title('Quad 4 Velocity from Accelerometer')
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Velocity (mm/s)')
    plt.legend()
    plt.savefig('ME457_HW1_P1.jpg', bbox_inches='tight')
    plt.show()


main()