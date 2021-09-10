## Introduction
A lightweight IOT framework for ESP32

## How To Install Firmware on your chip?
> Make sure you have installed **MicroPython** and **ampy** on your ESP32 chip.

1. Download or clone this repository. 
2. Update **WIFI_CONFIG** and **SERVER** in ```main.py```.
3. Type the command below and press enter.

```shell
ampy --port /dev/ttyUSB0 put main.py
```

Now, everything is ready!Enjoy it!

## 2021-09-10 ChangeLog:
- Installer of ESP32 chip
