#!usr/bin/env/python3
from nanpy import (ArduinoApi, SerialManager)
import time
import sys
import csv

text_filename = str(sys.argv[1]) + '_' + str(sys.argv[0] + '_ArdPoop')

header = 'time_millis, sensor_1, sensor_2, sensor_3,\
                       sensor_4, sensor_5, sensor_6,\
                       output_1, output_2, output_3,\
                       output_4, output_5, output_6,'
with open('{}.csv'.format(text_filename),'a') as sav_file:
    sav_file.write(header)

sensorPin1 = 14
sensorPin2 = 15
sensorPin3 = 16
sensorPin4 = 17
sensorPin5 = 18
sensorPin6 = 19

strain = lambda x : (1023-x)*(30000/1023)

try:
    # connection = SerialManager(device='/dev/ttyUSB0')
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")
    exit()
# Setup the pinModes as if we were in the Arduino IDE
a.pinMode(sensorPin1, a.INPUT)
a.pinMode(sensorPin2, a.INPUT)
a.pinMode(sensorPin3, a.INPUT)
a.pinMode(sensorPin4, a.INPUT)
a.pinMode(sensorPin5, a.INPUT)
a.pinMode(sensorPin6, a.INPUT)

# try:
    # Header
    # print('start_millis, sensor_1, strain_1, read_time')
while True:
    start = time.clock()
    sensor1 = a.analogRead(sensorPin1)
    sensor2 = a.analogRead(sensorPin2)
    sensor3 = a.analogRead(sensorPin3)
    sensor4 = a.analogRead(sensorPin4)
    sensor5 = a.analogRead(sensorPin5)
    sensor6 = a.analogRead(sensorPin6)
    output1 = strain(sensor1)
    output2 = strain(sensor2)
    output3 = strain(sensor3)
    output4 = strain(sensor4)
    output5 = strain(sensor5)
    output6 = strain(sensor6)
    end = time.clock()
    span = (end-start)*1000
    out_string = str(start) + ',' + str(sensor1) + ',' \
               + str(sensor2) + ',' + str(sensor3) + ',' \
               + str(sensor4) + ',' + str(sensor5) + ',' \
               + str(sensor6) + ',' + str(output1) + ',' \
               + str(output2) + ',' + str(output3) + ',' \
               + str(output4) + ',' + str(output5) + ',' \
               + str(output6) + ',' + str(span) + ',\n'
    with open('{}.csv'.format(text_filename),'a') as sav_file:
        sav_file.write(out_string)
        # print("{},{},{},{}".format(start,sensor1, output1, span))

# except:
#     print('Error')
