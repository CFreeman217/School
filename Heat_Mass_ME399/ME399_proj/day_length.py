## module day_length
import os, csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from findpeaks import findpeaks

def main():
    x_vals, y_vals = readFile('sun_data_short.txt', 0, -1, 1)
    tr_min, t_mean, tr_max = collect_weather_data('weather_data.txt')
    x_new = [i for i in range(1, len(x_vals)+1)]
    timehr = [time2hrs(i) for i in y_vals]
    max_day = timehr.index(max(timehr))
    max_hrs = max(timehr)
    min_day = timehr.index(min(timehr))
    min_hrs = min(timehr)
    print('MAX DAY: {}'.format(max_day))
    print('MAX HRS: {}'.format(max_hrs))
    print('MIN DAY: {}'.format(min_day))
    print('MIN HRS: {}'.format(min_hrs))
    max_deg_ang = 71.77 / (np.pi/180)
    min_deg_ang = 27.5 / (np.pi/180)
    max_deg_rad = max_deg_ang * np.pi/180
    min_deg_rad = min_deg_ang * np.pi/180
    amp = abs(max_deg_rad - min_deg_rad)/2
    k_shift = (max_deg_rad + min_deg_rad)/2
    period = 2*(max_day - min_day)
    b_coef = (2*np.pi) / period
    ang_func = lambda x : amp*np.cos(b_coef*(x - max_day))+k_shift
    d_x = butterworth_filter(t_mean,2000,40)
    sun_angles = [ang_func(i) for i in x_new]
    peaks = findpeaks(x_new, d_x)
    fp_ydata = [d_x[i] for i in peaks]

    # Plot 1

    plt.plot(x_new, t_mean, label='Mean Temperature')
    plt.plot(x_new, d_x, label='Filtered Temperature')
    plt.scatter(peaks, fp_ydata, label='Hottest Day: {}, July 22'.format(peaks[1]),c='r')
    # plt.plot(x_new,tr_min, label='95/% Confidence Lower Bound')
    # plt.plot(x_new, tr_max,label='95/% Confidence Upper Bound')
    plt.xlabel('Day of Year')
    plt.ylabel(r'Temperature ($^\circ$F)')
    plt.title('50-Mile Radius 10-Year Temperature Data')
    plt.legend()
    plt.savefig('ME399_Temp_Info.png', bbox_inches='tight')
    plt.show()

    # # Plot 2

    # plt.plot(x_new, timehr)
    # plt.scatter(max_day, max_hrs, color='r',label='June 21, Summer solstice')
    # plt.scatter(min_day, min_hrs, color='b',label='December 21, Winter Solstice')
    # plt.xlabel('Day of Year')
    # plt.ylabel('Hours of Daylight')
    # plt.title('Day Length')
    # plt.legend()
    # plt.savefig('ME399_day_length.png', bbox_inches='tight')
    # plt.show()

    # # Plot 3

    plt.plot(x_new, sun_angles)
    plt.scatter(196, ang_func(196), label=r'July 15 Peak Angle : {:1.2f}$^\circ$'.format(ang_func(196)),c='C1')
    plt.scatter(203, ang_func(203), label=r'July 22 Peak Angle: {:1.2f}$^\circ$'.format(ang_func(203)),c='C2')
    plt.scatter(258, ang_func(258), label=r'August 15 Peak Angle: {:1.2f}$^\circ$'.format(ang_func(258)),c='C3')
    plt.scatter(355, ang_func(355), label=r'December 21 Sun Angle: {:1.2f}$^\circ$'.format(ang_func(355)),c='b')
    plt.xlabel('Day of Year')
    plt.ylabel('Solar Noon Elevation (degrees)')
    plt.title('Kansas City Peak Elevation')
    plt.legend()
    plt.savefig('ME399_Sun_Trajectory.png', bbox_inches='tight')
    plt.show()

    # Plot 4



def collect_weather_data(data_file):
    '''
    One data point is the mean temp information across all available stations.
    Using this set, calculate a 95% confidence interval for the max temperature on each day.
    - remove leap day
    '''
    # Instantiate dictionary to hold weather data
    mean_data = {1:[]}
    r_95_l = []
    m_temp = []
    r_95_u = []
    # Open text file
    with open(data_file) as file:
        reader = csv.reader(file, delimiter=',')
        # Skip header row
        next(reader,None)
        data = list(reader)
    for d_line in range(len(data)):
        day_num = conv_date(data[d_line][5])
        h_temp = (data[d_line][8])
        if data[d_line][5].endswith('02-29'):
            continue
        if day_num in mean_data.keys():
            mean_data[day_num].append(h_temp)
        else:
            mean_data[day_num] = [h_temp,]
    for day in mean_data.keys():
        lower, mean, upper = mean95int(mean_data[day])
        r_95_l.append(lower)
        m_temp.append(mean)
        r_95_u.append(upper)
    return r_95_l, m_temp, r_95_u

def mean95int(y_list):
    ''' Generate the mean and a 95% confidence interval using student's t-distribution coefficient for a sample size between 30-50'''
    # Gather information about the data set
    y_list = [int(i) for i in y_list if i != '']
    n = len(y_list)
    tau = 1.960
    s_yi = sum(y_list)
    y_mean = s_yi/n
    # Sum of the squares of residuals from the mean
    s_sq_r = sum([(y_list[i] - y_mean)**2 for i in range(n)])
    # Standard deviation
    st_dev = (s_sq_r / (n-1))**(0.5)
    variance = tau*st_dev/((n)**(0.5))
    u_bnd = y_mean + variance
    l_bnd = y_mean - variance
    return l_bnd, y_mean, u_bnd

def readFile(fileName, col_x, col_y, skiprows):
    x_values = []
    y_values = []
    with open(fileName) as file:
        reader = csv.reader(file, delimiter=',')
        for _ in range(skiprows):
            next(reader, None)
        data = list(reader)
    for line in data:
        x_values.append(line[col_x])
        y_values.append(line[col_y])
    return x_values, y_values

def conv_date(in_date):
    num_days = {1:31,
                2:28,
                3:31,
                4:30,
                5:31,
                6:30,
                7:31,
                8:31,
                9:30,
                10:31,
                11:30,
                12:31}
    parse = in_date.split('-')
    month = int(parse[1])
    day = int(parse[2])
    today = day
    m_iter = 1
    while m_iter < month:
        today += num_days[m_iter]
        m_iter += 1
    return today

def time2hrs(in_time):
    parts = in_time.split(':')
    secs = float(parts[2])/3600
    mins = float(parts[1])/60
    return float(parts[0]) + secs + mins

def butterworth_filter(in_data, f_s=10000, f_c=50):
    '''
    Filters input data in butterworth plot to get rid of noise

    f_s : Sampling Frequency for the dataset
    f_c : Cutoff Frequency to eliminate noise
    '''
    W_n = 2 * f_c / f_s # Natural Frequency
    b, a = signal.butter(2, W_n)
    filtered_data = signal.filtfilt(b, a, in_data)
    return filtered_data

main()