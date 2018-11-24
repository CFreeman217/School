import os
import numpy as np, matplotlib.pyplot as plt

p_files = []

for file_name in os.listdir('.'):
    if file_name.endswith('_figure.png'):
        p_files.append(file_name[:-11])

for file_name in os.listdir('.'):
    if file_name.endswith('csv'):
        if file_name[:-4] not in p_files:
            # try:
            d_time, altitude, pit_sig, pit_meas, rol_sig, rol_meas, yaw_sig, yaw_meas,  = np.loadtxt(open(file_name),
                                            delimiter = ',',
                                            unpack = True,
                                            skiprows = 1,
                                            usecols = (1, 2, 30,31,32,33,34,35),)
            d_time /= 1000000
            altitude -= min(altitude)
        
            plt.plot(d_time[5:], altitude[5:], label='Altitude')
            plt.title('Altitude\n{}'.format(file_name))
            plt.xlabel('Time (s)')
            plt.ylabel('Altitude')
            plt.legend()
            # plt.savefig('{}_figure.png'.format(file_name[:-4]), bbox_inches='tight')
            plt.show()
            plt.plot(d_time[5:], pit_sig[5:], label='Signal')
            plt.plot(d_time[5:], pit_meas[5:], label='Measurement')
            plt.title('Pitch Command and Measure\n{}'.format(file_name))
            plt.xlabel('Time (s)')
            plt.ylabel('Pitch (Degrees)')
            plt.legend()
            # plt.savefig('{}_figure.png'.format(file_name[:-4]), bbox_inches='tight')
            plt.show()
            plt.plot(d_time[5:], rol_sig[5:], label='Signal')
            plt.plot(d_time[5:], rol_meas[5:], label='Measurement')
            plt.title('Roll Command and Measure\n{}'.format(file_name))
            plt.xlabel('Time (s)')
            plt.ylabel('Roll (Degrees)')
            plt.legend()
            # plt.savefig('{}_figure.png'.format(file_name[:-4]), bbox_inches='tight')
            plt.show()
            plt.plot(d_time[5:], yaw_sig[5:], label='Signal')
            plt.plot(d_time[5:], yaw_meas[5:], label='Measurement')
            plt.title('Yaw Command and Measure\n{}'.format(file_name))
            plt.xlabel('Time (s)')
            plt.ylabel('Yaw (Degrees/s)')
            plt.legend()
            # plt.savefig('{}_figure.png'.format(file_name[:-4]), bbox_inches='tight')
            plt.show()
            # except:
            #     pass
