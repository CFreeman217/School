import os
import numpy as np, matplotlib.pyplot as plt

p_files = []

for file_name in os.listdir('.'):
    if file_name.endswith('_figure.png'):
        p_files.append(file_name[:-11])

for file_name in os.listdir('.'):
    if file_name.endswith('csv'):
        if file_name[:-4] not in p_files:
            d_time, kpe, kiei, kded = np.loadtxt(open(file_name),
                                            delimiter = ',',
                                            unpack = True,
                                            skiprows = 1,
                                            usecols = (1, 35, 36, 37),)
            d_time /= 1000000
            plt.plot(d_time[5:], kpe[5:], label=r'K$_p$e')
            plt.plot(d_time[5:], kiei[5:], label=r'K$_i e_i$')
            plt.plot(d_time[5:], kded[5:], label=r'K$_d e_d$')
            plt.title('Gain Calibration\n{}'.format(file_name))
            plt.xlabel('time (s)')
            plt.ylabel('error')
            plt.legend()
            plt.savefig('{}_figure.png'.format(file_name[:-4]), bbox_inches='tight')
            plt.show()
