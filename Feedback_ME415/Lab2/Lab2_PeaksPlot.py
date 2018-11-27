import os
from scipy.signal import find_peaks
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import numpy as np

freq_data = {}
outFileName = 'M_values.csv'
with open(outFileName, 'w') as out_file:
    out_file.write('Freq(Hz),M-Value\n')

for file_name in os.listdir('.'):
    if file_name.endswith('Hz.xlsx'):
        wkbk = load_workbook(file_name)
        wkst = wkbk.active
        in_dat = []
        out_dat = []
        for row in range(2,wkst.max_row+1):
            cell_name = f'F{row}'
            in_dat.append(wkst[cell_name].value)
            cell_name = f'G{row}'
            out_dat.append(wkst[cell_name].value)
        peak_in = find_peaks(in_dat)
        peak_out = find_peaks(out_dat)
        # print(peak_in[0])
        M_val = np.mean(peak_out[0])/np.mean(peak_in[0])
        # freq_data[file_name] = {'COMMAND':in_dat,'OBSERVED':out_dat,'PEAK_IN':peak_in,'PEAK_OUT':peak_out,'M':M_val}
        outString = f'{file_name[5:-7]},{M_val},\n'
        with open(outFileName, 'a') as out_file:
            out_file.write(outString)