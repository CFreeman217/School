import os, math
import numpy as np, matplotlib.pyplot as plt
s_plot = 905
e_plot = 4005

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
    if file_name == 'clay_try_1529_Feb_18_06_22-0.csv':
        d_time, yaw, signal, filt_yaw = np.loadtxt(open(file_name),
                                        delimiter = ',',
                                        unpack = True,
                                        skiprows = 1,
                                        usecols = (1, 26, 30, 31),)

        d_time /= 1000000
        slopeline = lambda x : (x-39.6)*(-0.017)
        h_line = [0.01 for i in range(len(d_time))]
        newline = [slopeline(i) for i in d_time]
        filt_yaw2 = butter2(1,100,filt_yaw)
        filt_yaw2 = [(i/80)+.13 for i in filt_yaw2]
        # plt.plot(d_time[s_plot:], signal[s_plot:], label='Signal')
        # plt.plot(d_time[s_plot:], filt_yaw2[s_plot:], label='Butterworth Filtered Yaw')
        plt.plot(d_time[s_plot:e_plot], signal[s_plot:e_plot], label='Signal')
        plt.plot(d_time[s_plot:e_plot], filt_yaw2[s_plot:e_plot], label='Butterworth Filtered Yaw (1/80th Scale)')
        # plt.plot(d_time[s_plot:e_plot], h_line[s_plot:e_plot], c='r',linestyle=':')
        plt.plot(d_time[s_plot:e_plot], newline[s_plot:e_plot], c='r', linestyle=':')
        # plt.plot(d_time[5:], yaw[5:], label='Yaw')
        plt.title('Yaw and Response\nOpen Loop Gain Tuning')
        plt.xlabel('time (s)')
        plt.ylabel('Yaw Rate (Rad/s)')
        plt.axvline(x=33.6657,c='r',linestyle=':')
        plt.axvline(x=34.0702,c='r',linestyle=':')
        plt.ylim(-0.03,0.13)
        plt.grid(b=True, which='both')
        # plt.grid(b=True, which='major', axis='both')
        plt.legend(loc=3)
        plt.savefig('{}_A3figure.png'.format(file_name[:-4]), bbox_inches='tight')
        plt.show()
