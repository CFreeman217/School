import os, csv
# from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

def main():
    x_vals, y_vals = readFile('sun_data_short.txt', 0, -1, 1)
    x_new = [ i for i in range(1, len(x_vals)+1)]
    timehr = [time2hrs(i) for i in y_vals]
    max_day = timehr.index(max(timehr))
    max_hrs = max(timehr)
    min_day = timehr.index(min(timehr))
    min_hrs = min(timehr)
    plt.plot(x_new, timehr)
    plt.scatter(max_day, max_hrs, color='r')
    plt.scatter(min_day, min_hrs, color='b')
    plt.xlabel('Day of Year')
    plt.ylabel('Hours of Daylight')
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