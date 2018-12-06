import os, math
import numpy as np, matplotlib.pyplot as plt
from scipy import integrate

p_files = []

def butter2(f_c, f_s, in_list, highpass=False):
    '''
    2nd Order Butterworth Filter:
    f_c = cutoff frequency - adjust this to change amount of filtering
    f_s = sampling frequency - determined by the sampling rate of the dataset
    in_list = list of collected data points to be filtered
    '''
    gam = math.tan((math.pi*f_c)/f_s)
    coef_d = gam**2 + (2**0.5)*gam + 1
    a_1 = (2 * (gam**2 - 1)) / coef_d
    a_2 = (gam**2 - (2**0.5)*gam + 1)/coef_d
    if highpass:
        b_0 = 1
        b_1 = -2
        b_2 = 1
    else:
        b_0 = (gam**2) / coef_d
        b_1 = (2*b_0) / coef_d
        b_2 = b_0
    x_n1 = 0
    x_n2 = 0
    y_n1 = 0
    y_n2 = 0
    out_list = []
    for value in in_list:
        y_n = b_0*value + b_1*x_n1 + b_2*x_n2 - a_1*y_n1 - a_2*y_n2
        out_list.append(y_n)
        x_n2 = x_n1
        x_n1 = value
        y_n2 = y_n1
        y_n1 = y_n
    return out_list



for file_name in os.listdir('.'):
    if file_name.endswith('_figure.png'):
        p_files.append(file_name[:-11])

for file_name in os.listdir('.'):
    if file_name.endswith('csv'):
        if file_name[:-3] not in p_files:
            # try:
            st_plot = 500
            en_plot = 4500
            d_time, bar_altitude, z_accel, pit_sig, pit_meas, rol_sig, rol_meas, yaw_sig, yaw_meas,  = np.loadtxt(open(file_name),
                                            delimiter = ',',
                                            unpack = True,
                                            skiprows = 1,
                                            usecols = (1, 2, 23, 30, 31, 32, 33, 34, 35),)
            d_time /= 1000000
            d_time -= d_time[st_plot]
            bar_altitude -= bar_altitude[st_plot]
            bar_altitude += min(bar_altitude[st_plot:])*-1
            filt_alt = butter2(1,100,bar_altitude)
            filt_acc = butter2(1,100,z_accel)

            plt.plot(d_time[st_plot:en_plot], bar_altitude[st_plot:en_plot], label='Unfiltered')
            plt.plot(d_time[st_plot:en_plot], filt_alt[st_plot:en_plot], label='Filtered')
            plt.title('Barometer Altitude')
            plt.xlabel('Time (s)')
            plt.ylabel('Altitude (feet)')
            plt.legend()
            plt.savefig('Bar_altitude_figure.png'.format(file_name[:-4]), bbox_inches='tight')
            plt.show()
            plt.close()
            plt.plot(d_time[st_plot:en_plot], z_accel[st_plot:en_plot], label='Unfiltered')
            plt.plot(d_time[st_plot:en_plot], filt_acc[st_plot:en_plot], label='Filtered')
            plt.title('Accelerometer Altitude')
            plt.xlabel('Time (s)')
            plt.ylabel(r'Z-Acceleration (m/s$^2$)')
            plt.legend()
            plt.savefig('Acc_altitude_figure.png'.format(file_name[:-4]), bbox_inches='tight')
            plt.show()
            plt.close()
            plt.plot(d_time[st_plot:en_plot], pit_meas[st_plot:en_plot], label='Measurement')
            plt.plot(d_time[st_plot:en_plot], pit_sig[st_plot:en_plot], label='Command')
            plt.title('Pitch Command and Measurement')
            plt.xlabel('Time (s)')
            plt.ylabel('Pitch (Degrees)')
            plt.legend()
            plt.savefig('Pitch_figure.png'.format(file_name[:-4]), bbox_inches='tight')
            plt.show()
            plt.close()
            plt.plot(d_time[st_plot:en_plot], rol_meas[st_plot:en_plot], label='Measurement')
            plt.plot(d_time[st_plot:en_plot], rol_sig[st_plot:en_plot], label='Command')
            plt.title('Roll Command and Measurement')
            plt.xlabel('Time (s)')
            plt.ylabel('Roll (Degrees)')
            plt.legend()
            plt.savefig('Roll_figure.png'.format(file_name[:-4]), bbox_inches='tight')
            plt.show()
            plt.close()
            plt.plot(d_time[st_plot:en_plot], yaw_meas[st_plot:en_plot], label='Measurement')
            plt.plot(d_time[st_plot:en_plot], yaw_sig[st_plot:en_plot], label='Command')
            plt.title('Yaw Command and Measurement')
            plt.xlabel('Time (s)')
            plt.ylabel('Yaw (Radians per second)')
            plt.legend()
            plt.savefig('Yaw_figure.png'.format(file_name[:-4]), bbox_inches='tight')
            plt.show()
            plt.close()
            # except:
            #     pass
