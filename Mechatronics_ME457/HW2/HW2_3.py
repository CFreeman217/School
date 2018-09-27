#! usr/bin/env/python3

import numpy as np
import os, math
import matplotlib.pyplot as plt
from scipy import integrate, signal



def butterworth_filter(in_data, f_s=2, f_c=0.05):
    '''
    Filters input data in butterworth plot to get rid of noise

    f_s : Sampling Frequency for the dataset
    f_c : Cutoff Frequency to eliminate noise
    '''
    W_n = 2 * f_c / f_s # Natural Frequency
    b, a = signal.butter(2, W_n)
    filtered_data = signal.filtfilt(b, a, in_data)
    return filtered_data


# Run through the files in the current directory searching for the data file
for file_name in os.listdir('.'):
    # This method makes it easy to switch data files generated from the same trial scheme
    # if file_name.startswith('group2'):
    #     # Parse the data out and store the variables
    #     t_time, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z = np.loadtxt(open(file_name),
    #                                                                 delimiter=',',
    #                                                                 skiprows=2,
    #                                                                 unpack=True,
    #                                                                 usecols=(1,38,39,40,41,42,43))
    if file_name.startswith('MondayLab'):
        # Parse the data out and store the variables
        t_time, acc_x, acc_y, acc_z, gyr_y, gyr_x, gyr_z = np.loadtxt(open(file_name),
                                                                    delimiter=',',
                                                                    skiprows=2,
                                                                    unpack=True,
                                                                    usecols=(1,3,4,5,6,7,8))

# This holds the time since the trial began
dt_micros = [(t_time[k] - t_time[0])/1000000 for k, v in enumerate(t_time)]
# This holds the time since the last reading
delta_t = [t_time[k+1] - t_time[k] for k, v in enumerate(t_time[:-1])]
# We need to append a zero to get the same container size
delta_t = [0] + delta_t
# Generate integration function using simpsons adaptive trapezoidal method from scipy
gyr_p_xint = lambda a, b : integrate.trapz(gyr_x[a:b])
gyr_p_zint = lambda a, b : integrate.trapz(gyr_z[a:b])

# Store the cumulative integrals in lists
# gyr_xpts = [gyr_p_xint(0, k+1) for k, v in enumerate(dt_micros)]
# gyr_zpts = [gyr_p_zint(0, k+1) for k, v in enumerate(dt_micros)]

gyr_xpts = integrate.cumtrapz(gyr_x)
gyr_zpts = integrate.cumtrapz(gyr_z, dt_micros)

# Calculate the pitch angle from the integral and convert to degrees from radians
# gyr_pitch = [math.atan2(gyr_xpts[k], -gyr_zpts[k])*(180/math.pi) for k, v, in enumerate(dt_micros[:-1])]
gyr_pitch = [i * (180/math.pi) for i in gyr_zpts]
gyr_pitch = butterworth_filter(gyr_pitch)

# I know I could have written a for loop and saved a couple lines of code at this point but
# I am having a hard enough time learning C++ for the second problem in this homework.
acc_pitch = [math.atan2(acc_x[k], -acc_z[k])*(180/math.pi) for k, v, in enumerate(dt_micros)]

acc_pitch = butterworth_filter(acc_pitch)

# Plot
plt.plot(dt_micros, acc_pitch,label='Accelerometer Pitch')
plt.plot(dt_micros[:-1], gyr_pitch,'--',label='Gyroscope Pitch')
plt.title('Gyroscope vs. Accelerometer Readings')
plt.xlabel('Time (seconds)')
plt.ylabel('Pitch (degrees)')
plt.legend()
plt.savefig('ME457_HW2_3_v2.png', bbox_inches='tight')
plt.show()





