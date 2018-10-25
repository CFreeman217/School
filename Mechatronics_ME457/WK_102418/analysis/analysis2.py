import os
import numpy as np, matplotlib.pyplot as plt

p_files = []

for file_name in os.listdir('.'):
    if file_name.endswith('_figure.png'):
        p_files.append(file_name[:-11])

for file_name in os.listdir('.'):
    if file_name.endswith('csv'):
        if file_name[:-4] not in p_files:
            try:
                d_time, signal, yaw = np.loadtxt(open(file_name),
                                                delimiter = ',',
                                                unpack = True,
                                                skiprows = 1,
                                                usecols = (1, 30,31),)
                d_time /= 1000000
                plt.plot(d_time[5:], signal[5:], label='Signal')
                plt.plot(d_time[5:], yaw[5:], label='Yaw')
                plt.title('Yaw and Response\n{}'.format(file_name))
                plt.xlabel('time (s)')
                plt.ylabel('Yaw Rate (Rad/s)')
                plt.legend()
                plt.savefig('{}_figure.png'.format(file_name[:-4]), bbox_inches='tight')
                plt.show()
            except:
                pass
