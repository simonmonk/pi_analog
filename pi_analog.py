#squid.py Library

import RPi.GPIO as GPIO
import time, math

class PiAnalog:
	
    a_pin = 18
    b_pin = 23
    C = 0.30
    R1 = 1000
    

    def __init__(self, a_pin=18, b_pin=23, C=0.33, R1=1000):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.a_pin, self.b_pin, self.C, self.R1 = a_pin, b_pin, C, R1
        
    # empty the capacitor ready to start filling it up
    def discharge():
        GPIO.setup(self.a_pin, GPIO.IN)
        GPIO.setup(self.b_pin, GPIO.OUT)
        GPIO.output(self.b_pin, False)
        time.sleep(0.002) # 5T for 99% is 1.5mS
        
    # return the time taken for the voltage on the capacitor to count as a digital input HIGH
    # than means around 1.65V
    def charge_time():
        GPIO.setup(self.b_pin, GPIO.IN)
        GPIO.setup(self.a_pin, GPIO.OUT)
        GPIO.output(self.a_pin, True)
        t1 = time.time()
        while not GPIO.input(self.b_pin):
            pass
        t2 = time.time()
        return (t2 - t1) * 1000000 # microseconds

    # Take an analog reading as the time taken to charge after first discharging the capacitor
    def analog_read():
        self.discharge()
        t = self.charge_time()
        self.discharge()
        return t
        
    # Convert the time taken to charge the cpacitor into a value of resistance
    # To reduce errors, do it lots of times and take the average.
    def read_resistance():
        n = 10
        total = 0;
        for i in range(0, n):
            total = total + self.analog_read()
        t = total / float(n) # t is time to chanrge to Vt (1.65V) but we need time to charge to 0.63 Vs (2.1V) so * 2.1/1.65 or 1.26 to get Time constant T = RC
        T = t * 0.63 * 3.3 # RC = T = t * 1.26 ********* Measure Vt, reduce n to 1, measure C with meter, give really long discharge on C: 5T for 99% 5RC = 5 * 1k * 0.3u = 5 * 1 * 0.3m = 1.5 mS
        r = (T / C) - R1
        return r
        
    def read_temp_c(B=3800.0, R0=1000.0):
        R = self.read_resistance()
        t0 = 273.15     # 0 deg C in K
        t25 = t0 + 25.0 # 25 deg C in K
        # Steinhart-Hart equation - Google it
        inv_T = 1/t25 + 1/B * math.log(R/R0)
        T = (1/inv_T - t0)
        return T
        
    def read_temp_f(B=3800.0, R0=1000.0):
        return self.read_temp_c(B, R0) * 9 / 5 + 32
        