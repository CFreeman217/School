# standard libraries
import math, os
# external libraries (for convolve, sinc, arrays, csv parsing, and plotting)
import numpy as np, matplotlib.pyplot as plt

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

def fir_wind(f_c, t_b, in_list, highpass=False):
    '''
    Windowed sinc filter for low or high pass filtering using a blackman window
    f_c = cutoff frequency
    t_b = transition bandwidth
    in_list = list of collected data points to be filtered
    '''
    # big n
    b_n = int(math.ceil(4/t_b))
    if not b_n % 2 : b_n += 1 # make big n odd
    l_n = np.arange(b_n)

    # sinc filter calculation
    h = np.sinc(2 * f_c * (l_n - (b_n - 1) / 2.))

    # blackman window
    w = 0.42 - 0.5 * np.cos((2 * np.pi * l_n)/(b_n - 1)) + \
               0.08 * np.cos((4 * np.pi * l_n)/(b_n - 1))

    # combine sinc filter with blackman window
    h = h * w

    # normalize the filter to get unity gain
    h = h / sum(h)

    if highpass:
        # generate high pass filter through spectral inversion
        h = -h
        h[int((b_n - 1) / 2.)] += 1

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

d_time /= 1000000 # convert time from microseconds to milliseconds
cutoff = 1 # cutoff frequency
tran_band = 0.005 # transition bandwdth
sample = 100 # Sampling frequency is 100Hz

lp_acc = butter2(cutoff, sample, pitch_acc) # Filtered accelerometer
hp_gyro = butter2(cutoff, sample, pitch_gyro, highpass=True) # Filtered gyrometer

# lp_acc = fir_wind(cutoff, tran_band, pitch_acc) # Filtered accelerometer
# hp_gyr = fir_wind(cutoff, tran_band, pitch_gyro, highpass=True) # Filtered gyrometer

# Problem 1 plot
plt.plot(d_time, pitch_acc, label='Accelerometer')
plt.plot(d_time, -pitch_gyro,'--', label='Gyroscope')
plt.title('Accelerometer vs. Gyroscope Pitch Estimates')
plt.xlabel('Time (seconds)')
plt.ylabel('Pitch Estimate (degrees)')
plt.legend()
# plt.savefig('ME457_HW3_P1.png', bbox_inches='tight')
plt.show()

# Problem 2 plot
plt.plot(d_time, lp_acc[0:len(d_time)], label='Accelerometer LPF')
plt.plot(d_time, hp_gyr[0:len(d_time)], '--', label='Gyroscope HPF')
plt.title(r'Filter Convolution : f$_c$ = {}'.format(cutoff))
plt.xlabel('Time (seconds)')
plt.ylabel('Pitch Estimate (degrees)')
plt.legend()
# plt.savefig('ME457_HW3_P3.png', bbox_inches='tight')
plt.show()