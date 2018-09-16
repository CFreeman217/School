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
    l_n = np.arange(b_n)

    # sinc filter calculation
    sinc = lambda x : math.sin(math.pi*x)/(math.pi*x)
    h = sinc(2 * f_c * (l_n - (b_n - 1) / 2.))

    # blackman window
    w = 0.42 - 0.5 * math.cos((2 * math.pi * l_n)/(b_n - 1)) + \
               0.08 * math.cos((4 * math.pi * l_n)/(b_n - 1))

    # combine sinc filter with blackman window
    h = h * w

    # normalize the filter to get unity gain
    h = h / sum(h)

    # apply the filter to the signal
    sig = np.convolve(in_list, h)
    return sig

for file_name in os.listdir():
    if file_name.startswith('final'):
        d_time, pitch_acc, pitch_gyro = np.loadtxt(open(file_name),
                                            delimiter = ',',
                                            unpack = True,
                                            usecols = (1,30, 31),
                                            skiprows = 2)

d_time /= 1000 # convert time from microseconds to milliseconds
cutoff = 1 # cutoff frequency at 1Hz
sample = 100 # Sampling frequency is 100Hz
f_acc = butter2(cutoff, sample, pitch_acc) # Filtered accelerometer
f_gyro = butter2(cutoff, sample, pitch_gyro) # Filtered gyrometer

lp_acc = fir_wind_low(1, 0.08, pitch_acc)


# # Problem 1 plot
# plt.plot(d_time, pitch_acc, label='Accelerometer')
# plt.plot(d_time, -pitch_gyro,':', label='Gyroscope')
# plt.title('Accelerometer vs. Gyroscope Pitch Estimates')
# plt.xlabel('Time (milliseconds)')
# plt.ylabel('Pitch Estimate (degrees)')
# plt.legend()
# # plt.savefig('ME457_HW3_P1.png', bbox_inches='tight')
# plt.show()

# Problem 2 plot
plt.plot(d_time, pitch_acc, label='Accelerometer')
plt.plot(d_time, lp_acc,':', label='Low Pass Filter')
plt.title('Filter Convolution')
plt.xlabel('Time (milliseconds)')
plt.ylabel('Pitch Estimate (degrees)')
plt.legend()
plt.show()