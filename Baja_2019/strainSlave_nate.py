from nanpy import ArduinoApi
from nanpy import SerialManager
from nanpy import serial_manager
from time import sleep
serial_manager.connect('/dev/ttyACM0')

sensorPin = 14

try:
    connection = SerialManager(device='/dev/ttyACM0')
    #connection = SerialManager()
    a = ArduinoApi(connection = connection)
    print("Success")
except:
    print("Failed to connect to Arduino")

# Setup the pinModes as if we were in the Arduino IDE

a.pinMode(sensorPin, a.INPUT)

try:
    while True:
        sensor = a.analogRead(sensorPin)
        print("Signal Reading {}".format(sensor))
       
except:
    print('Error')
