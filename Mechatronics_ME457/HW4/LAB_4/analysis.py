import os
import numpy as np, matplotlib.pyplot as plt

for file_name in os.listdir('.'):
    if file_name.startswith('fucking_finally2'):
        d_time, r_acc, r_gyro, f_acc, f_gyro, f_comb = np.loadtxt(open(file_name),
                                        delimiter = ',',
                                        unpack = True,
                                        skiprows = 1,
                                        usecols = (1, 30, 31, 32, 33, 34),)

d_time /= 1000000

# plt.plot(d_time, r_gyro, label='Raw Data')
# plt.plot(d_time, f_gyro, label='Filtered Data')
# plt.title('Gyroscope Filtering Comparison')
# plt.xlabel('Time (s)')
# plt.ylabel(r'Pitch Angle ($^\circ$)')
# plt.legend()
# plt.savefig('gyro_filt_unfilt.png',bbox_inches = 'tight')
# plt.show()

# plt.plot(d_time, r_acc, label='Raw Data')
# plt.plot(d_time, f_acc, label='Filtered Data')
# plt.title('Accelerometer Filtering Comparison')
# plt.xlabel('Time (s)')
# plt.ylabel(r'Pitch Angle ($^\circ$)')
# plt.legend()
# plt.savefig('acc_filt_unfilt.png',bbox_inches = 'tight')
# plt.show()

# plt.plot(d_time, f_comb, label='Combined')
# plt.plot(d_time, f_acc, '--', label='Accelerometer', color='r')
# plt.plot(d_time, f_gyro, ':', label='Gyroscope')
# plt.title('Roll Angle Estimation Methods')
# plt.xlabel('Time (s)')
# plt.ylabel(r'Pitch Angle ($^\circ$)')
# plt.legend()
# plt.savefig('filt_est_methods.png',bbox_inches = 'tight')
# plt.show()

plt.plot(d_time, f_gyro, label='Filtered Data')
plt.title('Gyroscope Filtered Data Only')
plt.xlabel('Time (s)')
plt.ylabel(r'Pitch Angle ($^\circ$)')
plt.savefig('gyro_filt.png',bbox_inches = 'tight')
plt.show()
