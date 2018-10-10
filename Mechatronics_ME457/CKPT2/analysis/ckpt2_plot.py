import os
import numpy as np, matplotlib.pyplot as plt


for file_name in os.listdir('.'):
    if file_name.startswith('1009_try_1716_Sep_26_11_09-0.csv'):
        # if file_name[:-4] not in p_files:

        d_time, signal, pitch = np.loadtxt(open(file_name),
                                        delimiter = ',',
                                        unpack = True,
                                        skiprows = 1,
                                        usecols = (1, 38, 39),)
        pl_min = 1600 # Plot min range
        pl_max = 5500 # Plot max range
        re_min = 4120 # Begin calculating step response mean
        re_max = 4620 # End calculating step response mean
        d_time = (d_time - d_time[pl_min]) / 1000000
        pitch += 20
        mean_resp = [np.mean(pitch[re_min:re_max])]*(re_max - re_min)
        fifteen_rng = mean_resp[0]*1.15
        min_pitch = min(pitch[pl_min:pl_max])
        print('Mean at response region: {}'.format(mean_resp[0]))
        print('Maximum allowable overshoot: {}'.format(fifteen_rng))
        print('Overshoot point: {}'.format(min_pitch))
        plt.plot(d_time[pl_min:pl_max], signal[pl_min:pl_max],label='Signal')
        plt.plot(d_time[pl_min:pl_max], pitch[pl_min:pl_max], label=r'K$_p = 1.5\cdot10^{-3} , K_i = 2\cdot10^{-7}, K_d = 6.5\cdot10^{-4}$')
        plt.plot(d_time[re_min:re_max], mean_resp)
        plt.annotate('Step Input',xy=(25,-1),xytext=(32.5,-15),color='r',arrowprops=dict(arrowstyle='->',color='r'))
        plt.annotate('Step Input',xy=(30.5,-20),xytext=(32.5,-15),color='r',arrowprops=dict(arrowstyle='->',color='r'))
        plt.annotate('Step Input',xy=(34.5,-1),xytext=(32.5,-15),color='r',arrowprops=dict(arrowstyle='->',color='r'))
        plt.title('Tuned Controller Response')
        plt.xlabel('Time (s)')
        plt.ylabel(r'Pitch ($^\circ$)')
        plt.legend()
        plt.savefig('Prob4_fig.png', bbox_inches='tight')
        plt.show()

# for file_name in os.listdir('.'):
#     if file_name.startswith('1008_try_2142_Feb_11_14_40-0.csv'):
#         d_time, signal, pitch = np.loadtxt(open(file_name),
#                                         delimiter = ',',
#                                         unpack = True,
#                                         skiprows = 1,
#                                         usecols = (1, 38, 39),)
#         d_time /= 1000000
#         plt.plot(d_time[40:], pitch[40:],color='C1', label=r'K$_p = 2.5\cdot10^{-3} , K_i = 5\cdot10^{-8}, K_d = 6\cdot10^{-4}$')
#         plt.plot(d_time, signal,color='C0', label='Signal')
#         plt.title('Stability and Step input')
#         plt.xlabel('time (s)')
#         plt.ylabel(r'Pitch ($^\circ$)')
#         # plt.annotate('Disturbances',xy=(38.5,20),xytext=(28,60),color='r',arrowprops=dict(arrowstyle='->',color='r'))
#         # plt.annotate('Disturbances',xy=(44.5,-60),xytext=(28,60),color='r',arrowprops=dict(arrowstyle='->',color='r'))
#         # plt.annotate('Disturbances',xy=(50,20),xytext=(28,60),color='r',arrowprops=dict(arrowstyle='->',color='r'))
#         plt.legend()
#         plt.savefig('PROBLEM2_FIG.png', bbox_inches='tight')
#         plt.show()

