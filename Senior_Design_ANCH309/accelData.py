import os
import numpy as np, matplotlib.pyplot as plt

p_files = []

for file_name in os.listdir('.'):
    if file_name.endswith('_figure.png'):
        p_files.append(file_name[:-11])

for file_name in os.listdir('.'):
    if file_name.endswith('csv'):
        # if file_name[:-4] not in p_files:
        d_time, x_dat, y_dat, z_dat = np.loadtxt(open(file_name),
                                        delimiter = ',',
                                        unpack = True,
                                        skiprows = 1,
                                        usecols = (0,1,2,3))
        print(file_name)
       
        tot_dat = [(x_dat[i]**2+y_dat[i]**2+z_dat[i]**2)**0.5 for i in range(len(d_time))]
        print(max(tot_dat))
        # plt.plot(d_time, x_dat, label='x')
        plt.plot(d_time, tot_dat, label='Total Acceleration')
        # plt.plot(d_time, z_dat, label='z')
        # plt.plot(d_time, g_dat, label='g')
        plt.title('Accelerometer Data')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (g)')
        plt.legend()
        plt.savefig('{}_figure.png'.format(file_name[:-4]), bbox_inches='tight')
        plt.show()
