import os
import numpy as np, matplotlib.pyplot as plt

for file_name in os.listdir('.'):
    if file_name == 'try_1024_1632_Oct_02_06_35-0.csv':
        d_time, signal, yaw = np.loadtxt(open(file_name),
                                                delimiter = ',',
                                                unpack = True,
                                                skiprows = 1,
                                                usecols = (1, 30,31),)
        d_time /= 1000000
        old_pt = 0
        for point in range(len(d_time)):
            if old_pt == 0:
                if d_time[point] != 0:
                    print(d_time[point])
                    old_pt = d_time[point]

        plt.plot(d_time[5:], signal[5:], label='Signal')
        plt.plot(d_time[5:], yaw[5:], label='Yaw')
        plt.scatter(d_time[582], yaw[582], label='start')
        plt.title('Yaw and Response\n{}'.format(file_name))
        plt.xlabel('time (s)')
        plt.ylabel('Yaw Rate (Rad/s)')
        plt.legend()
        plt.savefig('{}_figure.png'.format(file_name[:-4]), bbox_inches='tight')
        plt.show()
