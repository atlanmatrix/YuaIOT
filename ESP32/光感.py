# 数字传感器
from machine import Pin

p36 = Pin(36, Pin.OUT)
if p36.value() == 1:
    print('Low light')
else:
    print('high light')

