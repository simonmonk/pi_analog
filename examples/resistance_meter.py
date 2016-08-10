import * from PiAnalog
import time

p = PiAnalog()

while True:
    print(p.read_resistance())
    time.sleep(1)
    