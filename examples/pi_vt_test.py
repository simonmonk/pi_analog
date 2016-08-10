# Apply between 0 and 3.3V to pin 18 and note the voltage at wchich the input registers as high.

import RPi.GPIO as GPIO
import time

a_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(a_pin, GPIO.IN)

while True:
    while not GPIO.input(a_pin):
        pass
    print("Pin HIGH: Note Vth")
    while GPIO.input(a_pin):
        pass
    print("Pin LOW: Note Vtl")
    