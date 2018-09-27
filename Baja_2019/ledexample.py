import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # Sets GPIO pin names using the broadcom scheme

# LED attached from GPIO pin 18 through 330 ohm resistor to ground

GPIO.setup(18, GPIO.OUT) # Set pin 18 as output

GPIO.output(18, GPIO.HIGH)

time.sleep(2)

GPIO.output(18, GPIO.LOW)

GPIO.cleanup()





