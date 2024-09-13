import utime
from machine import Pin
from time import time_ns


pulse_pin = Pin(15, Pin.IN, Pin.PULL_DOWN)
print(pulse_pin.value())


