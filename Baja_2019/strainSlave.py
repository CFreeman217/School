#!usr/bin/env/python3
from nanpy import (ArduinoApi, SerialManager)
import time

sensorPin = 14
strain = lambda x : (1023-x)*(30000/1023)

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
    print('start_millis, sensor_1, strain_1, read_time')
    while True:
        start = time.clock()
        sensor1 = a.analogRead(sensorPin)
        end = time.clock()
        output1 = strain(sensor1)
        span = (end-start)*1000
        print("{},{},{},{}".format(start,sensor1, output1, span))
       
except:
    print('Error')
