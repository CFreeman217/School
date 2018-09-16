#!usr/bin/env/python3
from nanpy import (ArduinoApi, SerialManager)
from time import sleep

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
    while True:
        sensor1 = a.analogRead(sensorPin)
        print("Signal Reading {}".format(sensor1))
       
except:
    print('Error')