# Pin:
# GND, VCC
# MOT - 输入高电平触发震动
# LED - LED 灯供电

from machine import Pin

# Pin 23 connect to MOT
p23 = Pin(23, Pin.OUT)
p23.value(1)
