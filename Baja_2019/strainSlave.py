#!usr/bin/env/python3
from nanpy import (ArduinoApi, SerialManager)
import math
import timeit
import time

sensorPin = 14

try:
    # connection = SerialManager(device='/dev/ttyUSB0')
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")
    exit()
# Setup the pinModes as if we were in the Arduino IDE
a.pinMode(sensorPin, a.INPUT)

try:
    # Header
    print('start_millis, sensor_1, strain_1, end_millis, read_time')
    while True:
        start = datetime.time()
        sensor1 = a.analogRead(sensorPin)
        end = datetime.time()
        strain1 = (1023-sensor1)*(30000/1023)
        span = end-start
        print("{},{},{},{},{}".format(start,sensor1, strain1, end, span))
       
except:
    print('Error')
