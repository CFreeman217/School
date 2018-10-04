import math
import os, numpy as np, matplotlib.pyplot as plt

def butter2(f_c, f_s, in_list):
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

def convolve(filt_list, data_list):
    len_f = len(filt_list)
    len_d = len(data_list)
    out_list = []
    if len_d > len_f:
        for key in range(len_d):
            pass




def fir_wind_low(f_c, t_b, in_list):
    '''
    Windowed sinc filter for low pass filtering using a blackman window
    f_c = cutoff frequency
    t_b = transition bandwidth
    in_list = list of collected data points to be filtered
    '''
    # big n
    b_n = int(math.ceil(4/t_b))
    if not b_n % 2 : b_n += 1 # make big n odd


    s_sz = len(in_list)
    d_sum = sum(in_list)
    sinc = lambda x : math.sin(math.pi*x)/(math.pi*x)
    blackman = lambda x : 0.42 - 0.5*math.cos((2*math.pi*x)/(s_sz-1)) + 0.08*math.cos((4*math.pi*n)/(s_sz-1))
    h_norm = []
    out_list = []
    for item in in_list:
        in_num = 2*f_c*(item - (s_sz - 1)/2)
        h_n = sinc(in_num)*blackman(item)

for file_name in os.listdir():
    if file_name.startswith('final'):
        d_time, pitch_acc, pitch_gyro = np.loadtxt(open(file_name),
                                            delimiter = ',',
                                            unpack = True,
                                            usecols = (1,30, 31),
                                            skiprows = 2)

d_time /= 1000
cutoff = 1
sample = 100
f_acc = butter2(cutoff, sample, pitch_acc)
f_gyro = butter2(cutoff, sample, pitch_gyro)

plt.plot(d_time, pitch_acc, label='Accelerometer')
plt.plot(d_time, -pitch_gyro,':', label='Gyroscope')
plt.title('Accelerometer vs. Gyroscope Pitch Estimates')
plt.xlabel('Time (milliseconds)')
plt.ylabel('Pitch Estimate (degrees)')
plt.legend()
plt.savefig('ME457_HW3_P1.png', bbox_inches='tight')
plt.show()
