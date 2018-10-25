import os
import numpy as np, matplotlib.pyplot as plt

# p_files = []

# for file_name in os.listdir('.'):
#     if file_name.endswith('_figure.png'):
#         p_files.append(file_name[:-11])

# for file_name in os.listdir('.'):
#     if file_name.startswith('1008_try_2149_Feb_11_14_47-0.csv'):
#         # if file_name[:-4] not in p_files:

#         d_time, signal, pitch = np.loadtxt(open(file_name),
#                                         delimiter = ',',
#                                         unpack = True,
#                                         skiprows = 1,
#                                         usecols = (1, 38, 39),)
#         d_time /= 1000000
#         # plt.plot(d_time, signal, label='Signal')
#         plt.plot(d_time[40:], pitch[40:], label=r'K$_p = 2.5\cdot10^{-3} , K_i = 5\cdot10^{-8}, K_d = 6\cdot10^{-4}$')
#         plt.title('Disturbance Response')
#         plt.xlabel('time (s)')
#         plt.ylabel(r'Pitch ($^\circ$)')
#         plt.annotate('Disturbances',xy=(38.5,20),xytext=(28,60),color='r',arrowprops=dict(arrowstyle='->',color='r'))
#         plt.annotate('Disturbances',xy=(44.5,-60),xytext=(28,60),color='r',arrowprops=dict(arrowstyle='->',color='r'))
#         plt.annotate('Disturbances',xy=(50,20),xytext=(28,60),color='r',arrowprops=dict(arrowstyle='->',color='r'))
#         plt.legend()
#         plt.savefig('PROBLEM3_FIG.png', bbox_inches='tight')
#         plt.show()

for file_name in os.listdir('.'):
    if file_name.startswith('1008_try_2142_Feb_11_14_40-0.csv'):
        d_time, signal, pitch = np.loadtxt(open(file_name),
                                        delimiter = ',',
                                        unpack = True,
                                        skiprows = 1,
                                        usecols = (1, 38, 39),)
        d_time /= 1000000
        plt.plot(d_time[40:], pitch[40:],color='C1', label=r'K$_p = 2.5\cdot10^{-3} , K_i = 5\cdot10^{-8}, K_d = 6\cdot10^{-4}$')
        plt.plot(d_time, signal,color='C0', label='Signal')
        plt.title('Stability and Step input')
        plt.xlabel('time (s)')
        plt.ylabel(r'Pitch ($^\circ$)')
        # plt.annotate('Disturbances',xy=(38.5,20),xytext=(28,60),color='r',arrowprops=dict(arrowstyle='->',color='r'))
        # plt.annotate('Disturbances',xy=(44.5,-60),xytext=(28,60),color='r',arrowprops=dict(arrowstyle='->',color='r'))
        # plt.annotate('Disturbances',xy=(50,20),xytext=(28,60),color='r',arrowprops=dict(arrowstyle='->',color='r'))
        plt.legend()
        plt.savefig('PROBLEM2_FIG.png', bbox_inches='tight')
        plt.show()

