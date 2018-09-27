import re, os
import numpy as np

data_regex = re.compile(r'''(
    (\d+)
    (Volt)
)''', re.VERBOSE)

def main():
    for file_name in os.listdir('.'):
        if file_name.endswith('Volt.txt'):
            # [0] = Full name
            # [1] = Voltage
            # [2] = 'volt'
            trial_info = data_regex.findall(file_name)
            if trial_info[0][2] == 'Volt':
                time, voltage = np.loadtxt(open(file_name),
                                    delimiter='\t',
                                    unpack=True)
                t_data = []
                v_data = []
                t_off_t = 0
                toggle = 0
                for i in range(len(time)):
                    if voltage[i] > 0:
                        t_data.append(time[i])
                        v_data.append(voltage[i])
                        if t_off_t == 0:
                            time_offset = time[i-1]
                            t_off_t = 1
                if v_data:
                    v_max = v_data[-1]
                    v_tau = (1-1/np.exp(1))*v_max
                    t_data = [i - time_offset for i in t_data]
                    totaltime = t_data[-1]
                for i in range(len(v_data)):
                    if v_data[i] > v_tau and toggle == 0:
                        toggle += 1
                        print('Test Voltage: {}\nTime Constant: {}'.format(trial_info[0][1],t_data[i]))
                        print('Total Time : {}'.format(totaltime))

main()