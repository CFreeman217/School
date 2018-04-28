import os, csv
# from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

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
    sun_angles = [ang_func(i) for i in x_new]

    # Plot 1

    plt.plot(x_new, timehr)
    plt.scatter(max_day, max_hrs, color='r',label='June 21, Summer solstice')
    plt.scatter(min_day, min_hrs, color='b',label='December 21, Winter Solstice')
    plt.xlabel('Day of Year')
    plt.ylabel('Hours of Daylight')
    plt.title('Day Length')
    plt.legend()
    plt.savefig('ME399_day_length.png', bbox_inches='tight')
    plt.show()

    # Plot 2

    plt.plot(x_new, sun_angles)
    plt.xlabel('Day of Year')
    plt.ylabel('Sun Path Angle (degrees)')
    plt.title('Kansas City Yearly Sun Trajectory')
    plt.savefig('ME399_Sun_Trajectory.png', bbox_inches='tight')
    plt.show()

    # Plot 3

    plt.plot(x_new, t_mean, label='Mean Temperature')
    plt.plot(x_new,tr_min, label='95/% Confidence Lower Bound')
    plt.plot(x_new, tr_max,label='95/% Confidence Upper Bound')
    plt.xlabel('Day of Year')
    plt.ylabel('Temperature (F)')
    plt.title('50-Mile 10-Year Temperature Data')
    plt.legend()
    plt.savefig('ME399_Temp_Info.png', bbox_inches='tight')
    plt.show()




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
        lower, mean, upper = do_math(mean_data[day])
        r_95_l.append(lower)
        m_temp.append(mean)
        r_95_u.append(upper)
    return r_95_l, m_temp, r_95_u

def do_math(y_list):
    # Gather information about the data set
    y_list = [int(i) for i in y_list if i != '']
    n = len(y_list)
    s = n-1
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

'''
TAVG = Average Temperature
TMAX = Max Temperature
TMIN = Min Temperature
TOBS = Temp. at time of observation?
'''



main()