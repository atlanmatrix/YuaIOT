import os
import json
import time
import socket
import machine
import network
import urequests
from time import sleep

# All external methods should import via middle
from middle_man import *

VERSION = '0.0.1.002'
ap = None

def update(comp='main'):
    res = urequests.get('http://192.168.31.54:8899/update/' + comp)
    json_res = res.json()

    print(res.json())
    print(res.status_code)
    print(dir(res))
    # json_res = json.loads(res.text)
    if res.status_code == 200:
        if json_res.get('is_suc'):
            data = json_res['data']
            f = open(data['path'], 'w')
            f.write(data['content'])
            f.close()
            print('Update ' + data['path'] + ' successfully!')
            print('Waiting for reset...')
            sleep(2)
            machine.reset()
        else:
            print('Request Error: ' + json_res.get('msg'))
    else:
        print('HTTP Error: ' + str(res.status_code))


def create_ap():
    # Create access point for connection
    global ap
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    try:
        ap_config = {'essid': 'ESP32_' + random_hex_str}
        ap.config(essid=ap_config['essid'])
        ap.active(True)
    except:
        pass


# def connect():
#     ssid = 'Xiaomi_CCD8'
#     passwd = 'Mxsoft@806'
#     sta = network.WLAN(network.STA_IF)
#     sta.active(True)
#     sta.connect(ssid, passwd)


# def update():

#     res = urequests.get('http://192.168.31.54:8899/update/xxxx')
#     data = json.loads(res.text)['data']
#     f = open('./main.py', 'w')
#     f.write(data)
#     f.close()
#     machine.reset()


# def backup_firmware():
#     pass


# def restore_firmware():
#     pass


# connect()
create_ap()
