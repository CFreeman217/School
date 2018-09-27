import os
import re
import numpy as np
import matplotlib.pyplot as plt

def main():
    for file_name in os.listdir('.'):
        time, temp = np.loadtxt(file_name,
                                unpack=True,
                                skiprows=1)
        plt.plot(time,temp)
        plt.xlabel('Time')
        plt.ylabel('Temp. Reading')
        plt.title(file_name)
        plt.show()
main()