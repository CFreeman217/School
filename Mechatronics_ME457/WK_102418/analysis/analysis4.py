import os, math
import numpy as np, matplotlib.pyplot as plt
# Start and end plot data points
s_plot = 200
e_plot = 875

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
    if file_name == 'Sep_20_21_37-0.csv':
        d_time, yaw, signal, filt_yaw = np.loadtxt(open(file_name),
                                        delimiter = ',',
                                        unpack = True,
                                        skiprows = 1,
                                        usecols = (1, 26, 30, 31),)
        # Convert time to seconds
        d_time /= 1000000
        # Butterworth filtering on gyro output data that came in with lots of noise
        filt_yaw2 = butter2(1,100,filt_yaw)
        # Adjust and scale the filtered yaw data to overlay with the signal input
        filt_yaw2 = [(i+.1) for i in filt_yaw2]
        # Plot signal and yaw data
        plt.plot(d_time[s_plot:e_plot], signal[s_plot:e_plot], label='Signal')
        plt.plot(d_time[s_plot:e_plot], filt_yaw2[s_plot:e_plot], label='Yaw Measured')
        plt.title('Yaw and Response\nClosed Loop Gain Optimized')
        plt.xlabel('Time (s)')
        plt.ylabel('Yaw Rate (Rad/s)')
        plt.legend()
        plt.savefig('ckpt_fig2.png')
        plt.show()
