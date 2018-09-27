import os
import numpy as np, matplotlib.pyplot as plt

for file_name in os.listdir('.'):
    if file_name.startswith('trial'):
        d_time, kpe, kiei, kded = np.loadtxt(open(file_name),
                                        delimiter = ',',
                                        unpack = True,
                                        skiprows = 1,
                                        usecols = (1, 35, 36, 37),)