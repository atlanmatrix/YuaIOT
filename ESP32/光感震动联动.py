# 光感震动
from machine import Pin


p23 = Pin(23, Pin.OUT)
p36 = Pin(36, Pin.IN)

while True:
    if p36.value() == 0:
        p23.value(1)
    else:
        p23.value(0)
