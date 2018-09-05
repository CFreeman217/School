#! usr/bin/env/python3

import numpy as np
import os, math
import matplotlib.pyplot as plt
from scipy import integrate

# Run through the files in the current directory searching for the data file
for file_name in os.listdir('.'):
    # This method makes it easy to switch data files generated from the same trial scheme
    if file_name.startswith('group2'):
        # Parse the data out and store the variables
        t_time, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z = np.loadtxt(open(file_name),
                                                                    delimiter=',',
                                                                    skiprows=2,
                                                                    unpack=True,
                                                                    usecols=(1,38,39,40,41,42,43))

# This holds the time since the trial began
dt_micros = [t_time[k] - t_time[0] for k, v in enumerate(t_time)]
# This holds the time since the last reading
delta_t = [t_time[k+1] - t_time[k] for k, v in enumerate(t_time[:-1])]
# We need to append a zero to get the same container size
delta_t = [0] + delta_t

# Generate integration function using simpsons adaptive trapezoidal method from scipy
gyr_p_xint = lambda a, b : integrate.simps(gyr_x[a:b], dt_micros[a:b])
gyr_p_zint = lambda a, b : integrate.simps(gyr_z[a:b], dt_micros[a:b])

# Store the cumulative integrals in lists
gyr_xpts = [gyr_p_xint(0, k+1) for k, v in enumerate(dt_micros)]
gyr_zpts = [gyr_p_zint(0, k+1) for k, v in enumerate(dt_micros)]

# Calculate the pitch angle from the integral and convert to degrees from radians
gyr_pitch = [math.atan2(gyr_zpts[k], gyr_xpts[k])*(180/math.pi) for k, v, in enumerate(dt_micros)]

# I know I could have written a for loop and saved a couple lines of code at this point but
# I am having a hard enough time learning C++ for the second problem in this homework.
acc_pitch = [math.atan2(acc_z[k], acc_x[k])*(180/math.pi)+90 for k, v, in enumerate(dt_micros)]

# It turns out that time is in microseconds so convert to seconds
dt_micros = [i/1000000 for i in dt_micros]

# Plot
plt.plot(dt_micros, acc_pitch,'--b',label='Accelerometer Pitch')
plt.plot(dt_micros, gyr_pitch,'r',label='Gyroscope Pitch')
plt.title('Gyroscope vs. Accelerometer Readings')
plt.xlabel('Time (seconds)')
plt.ylabel('Pitch (degrees)')
plt.legend()
plt.savefig('ME457_HW2_3.jpg', bbox_inches='tight')
plt.show()






