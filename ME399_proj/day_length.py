import os, csv
# from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

def main():
    x_vals, y_vals = readFile('sun_data_short.txt', 0, -1, 1)
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
    max_deg_ang = 71.77
    min_deg_ang = 27.5
    # max_deg_rad = max_deg_ang * np.pi/180
    max_deg_rad = max_deg_ang
    min_deg_rad = min_deg_ang
    amp = abs(max_deg_rad - min_deg_rad)/2
    k_shift = (max_deg_rad + min_deg_rad)/2
    period = 2*(max_day - min_day)
    b_coef = (2*np.pi) / period
    ang_func = lambda x : amp*np.cos(b_coef*(x - max_day))+k_shift
    sun_angles = [ang_func(i) for i in x_new]
    plt.plot(x_new, timehr)
    plt.plot(x_new, sun_angles)
    plt.scatter(max_day, max_hrs, color='r')
    plt.scatter(min_day, min_hrs, color='b')
    plt.xlabel('Day of Year')
    plt.ylabel('y-axis label')
    plt.title('Kansas City Yearly Daylight Hours')
    plt.show()

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

def time2hrs(in_time):
    parts = in_time.split(':')
    secs = float(parts[2])/3600
    mins = float(parts[1])/60
    return float(parts[0]) + secs + mins


main()