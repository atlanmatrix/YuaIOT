# 步进电机驱动
from machine import Pin
import time


pin_32 = Pin(32, Pin.OUT)
pin_33 = Pin(33, Pin.OUT)
pin_25 = Pin(25, Pin.OUT)
pin_26 = Pin(26, Pin.OUT)


def forward(delay):
    # 必须按（IN）顺序通电
    setStep(1, 0, 0, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 0)
    time.sleep(delay)
    setStep(0, 0, 1, 0)
    time.sleep(delay)
    setStep(0, 0, 0, 1)
    time.sleep(delay)


def setStep(w1, w2, w3, w4):
    pin_25.value(w1)
    pin_33.value(w2)
    pin_26.value(w3)
    pin_32.value(w4)


def main(delay):
    while True:
        forward(int(delay) / 1000.0)
         
main() # 调用main
