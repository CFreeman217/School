import os, math
import numpy as np, matplotlib.pyplot as plt

# For complementary filtering sensor fusion.
# Sampling frequency is determined by the dataset.
# Cutoff frequency must be the same for both sensors.
f_c = .5
savefiles = True

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

# Parse CSV data file
for file_name in os.listdir('.'):
    if file_name.endswith('Fusion.csv'):
        dtime, acc_y, acc_z, gyro = np.loadtxt(open(file_name),
                                            delimiter = ',',
                                            unpack = True,
                                            skiprows = 1,
                                            usecols = (0, 1, 2, 3),)
# Gathering actual sampling time information for numeric integration
# This handles the case that the information comes from a device
# that samples at a different rate from the stuff we have been doing
# in class
t_samp = [dtime[i+1] - dtime[i] for i in range(len(dtime)-1)]
f_samp = np.mean(t_samp)

# Generat the roll estimate using the atan2 method from the accelerometer
rollA = [math.atan2(acc_y[i], -acc_z[i])*(180/math.pi) for i in range(len(dtime))]

# Numeric integration by trapezoidal formula
trap = lambda h, f_0, f_1 : h * (f_0 - f_1) / 2

# instantiate a buffer and create an empty list for roll estimate
roll0 = 0
rollG = []

# generate gyro datapoints using trapezoidal method
for i in range(1,len(gyro)):
    roll0  = roll0 + trap(f_samp, gyro[i], gyro[i-1])*(180/math.pi)
    rollG.append(roll0)

# filtering function calls
filt_rollA = butter2(f_c, 1/f_samp, rollA)
filt_rollG = butter2(f_c, 1/f_samp, rollG, highpass=True)
comp_filtAG = [filt_rollA[i] + filt_rollG[i] for i in range(len(filt_rollG))]

plt.plot(dtime, rollA, label='Raw Accelerometer Estimate')
plt.plot(dtime, filt_rollA, label=r'F$_c = {}Hz, F_s = {:1.2f}Hz$'.format(f_c, 1/f_samp))
plt.xlabel('Time (s)')
plt.ylabel(r'Roll Angle ($^\circ$)')
plt.title('4(a) : Low Pass Butterworth Filter Roll Angle')
plt.legend()
if savefiles:
    plt.savefig('prob4a.png',bbox_inches='tight')
plt.show()

plt.plot(dtime[:len(rollG)], rollG, label='Raw Gyroscope Estimate')
plt.plot(dtime[:len(filt_rollG)], filt_rollG, label=r'F$_c = {}Hz, F_s = {:1.2f}Hz$'.format(f_c, 1/f_samp))
plt.xlabel('Time (s)')
plt.ylabel(r'Roll Angle ($^\circ$)')
plt.title('4(b) : High Pass Butterworth Filter Roll Angle')
plt.legend()
if savefiles:
    plt.savefig('prob4b.png',bbox_inches='tight')
plt.show()

plt.plot(dtime[:len(comp_filtAG)],comp_filtAG, label='Complementary Filter' )
plt.plot(dtime, filt_rollA,'--', label='Accelerometer Estimate')
plt.plot(dtime[:len(filt_rollG)], filt_rollG,':', label='Gyroscope Estimate')
plt.xlabel('Time (s)')
plt.ylabel(r'Roll Angle ($^\circ$)')
plt.title('4(c) : Sensor Fusion Roll Estimate')
plt.legend()
if savefiles:
    plt.savefig('prob4c.png',bbox_inches='tight')
plt.show()