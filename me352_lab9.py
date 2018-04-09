import os
import numpy as np
import matplotlib.pyplot as plt

def main():
    if 'Specimen_RawData_1.csv' in os.listdir('.'):
        x, y = np.loadtxt(open('Specimen_RawData_1.csv'),
                                        delimiter=',',
                                        skiprows=4,
                                        unpack=True,
                                        usecols=(0,2))
        x += 4 # Time shift (seconds)
        plt.plot(x,y,label='LabVIEW Data')
    if 'Instron_VI_Data.csv' in os.listdir('.'):
        x, y = np.loadtxt(open('Instron_VI_Data.csv'),
                                        delimiter=',',
                                        skiprows=1,
                                        unpack=True)
        y *= 4.44822 # Convert psi to MPa
        plt.plot(x,y,label='Instron Data',color='r')
    plt.title('Instron vs Labview Strain Gauge Data')
    plt.xlabel('Time (s)')
    plt.ylabel('Load (N)')
    # plt.ylabel('Strain ($\mu$$\epsilon$)')
    plt.legend(loc='upper left')
    # plt.savefig('me352_instLab9.png', bbox_inches='tight')
    plt.show()





main()