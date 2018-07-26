#! /usr/bin/env python3
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    for filename in os.listdir('.'):
        if filename.startswith("ArduinoPoop"):
            print("HEY")
            pt, a0, a1, a2, c_time, wt = np.loadtxt(open(filename),
                                                    delimiter=',',
                                                    skiprows=1,
                                                    unpack=True)
            c_time = c_time/1000
            plt.plot(c_time, a0,label='Analog Pin 0')
            plt.plot(c_time, a1,label='Analog Pin 1')
            plt.plot(c_time, a2,label='Analog Pin 2')
            plt.xlabel('Time (s)')
            plt.ylabel('Reading')
            plt.legend()
            plt.show()

main()

