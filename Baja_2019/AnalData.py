#! /usr/bin/env python3
import os
import numpy as np

import matplotlib.pyplot as plt


def main():
    for filename in os.listdir('.'):
        if filename.endswith(".csv"):
            print('Processing Detected .csv File... {}'.format(filename))
            pt, a2, a1, a0, c_time, wt = np.loadtxt(open(filename),
                                                    delimiter=',',
                                                    skiprows=1,
                                                    unpack=True)
            c_time = c_time/1000
            plt.plot(c_time, a0,label='Analog Pin 0')
            plt.plot(c_time, a1,label='Analog Pin 1')
            plt.plot(c_time, a2,label='Analog Pin 2')
            plt.title('Analog Readings: {}'.format(filename))
            plt.xlabel('Time (s)')
            plt.ylabel('Reading')
            plt.legend()
            plt.show()
            # plt.savefig('Graph_{}.jpg'.format(filename),box_inches='tight')

main()

