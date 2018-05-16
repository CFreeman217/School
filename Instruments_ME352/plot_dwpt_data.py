from openpyxl import load_workbook
import matplotlib.pyplot as plt
import numpy as np
def col(number):
    '''Takes a column number and returns the corresponding letter value'''
    alphabet = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return alphabet[number]

wkbk = load_workbook('DeadWeightPressureTesterData.xlsx')
wkst = wkbk.active
trial_data = {}
mean_data = []
for point in range(2,25):
    sum_point = 0
    for trial in range(3,23):
        sum_point += wkst['{}{}'.format(col(point), trial)].value
    mean_data.append(sum_point/20)
print(mean_data)
for trial in range(3,23):
    x_points = []
    y_points = []
    for point in range(2,25):
        x_points.append(wkst['{}{}'.format(col(point), 2)].value)
        y_points.append(wkst['{}{}'.format(col(point), trial)].value)
    trial_data[trial-2] = [x_points, y_points]


for trial in trial_data:
    print('Trial Number = {}'.format(trial))
    plt.plot(trial_data[trial][0], trial_data[trial][1])
    


plt.title('DWPT Calibration Data')
plt.xlabel('Pressure (lbm)')
plt.ylabel('Voltage')

plt.show()