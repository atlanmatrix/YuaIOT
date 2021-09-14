"""
WARNING: 
ALL exists files and settings will be removed after you invoke `run` method, and
firmwares will be entirely new installed.
"""
import os
import json
import network
import urequests
import machine
from time import sleep
from network import STAT_CONNECTING, STAT_NO_AP_FOUND, STAT_WRONG_PASSWORD
from network import STAT_HANDSHAKE_TIMEOUT
import collector_app


ROLE = 2
VERSION = "0.0.1.0909"
WIFI_CONFIG = {'ssid': '', 'passwd': ''}
SERVER = 'http://iot.yua.im'


def simple_log(msg=None):
    if msg is None:
        with open('sys.log', 'r') as fd:
            data = fd.read()
            line_no = 1

            lines = data.split('\n')
            max_space = len(str(len(lines))) + 2
            for line in lines:
                print(str(line_no) + ' ' * (max_space - len(str(line_no))) + line)
                line_no += 1
    else:
        with open('sys.log', 'a') as fd:
            fd.write(msg + '\n')


def simple_connect():
    ssid = WIFI_CONFIG['ssid']
    passwd = WIFI_CONFIG['passwd']

    sta = network.WLAN(network.STA_IF)

    if sta.status() == STAT_CONNECTING:
        print('[Connecting]: this may take a few seconds...')
        sleep(1)
        return simple_connect()
    elif sta.status() in [STAT_NO_AP_FOUND, STAT_WRONG_PASSWORD]:
        return print('[Fatal error]: ssid not found or password incorrect!')
    elif sta.status() == STAT_HANDSHAKE_TIMEOUT:
        return print('[Error]: timeout!')
    elif sta.isconnected():
        return print('[Success]: Connect Wi-Fi successfully')
    else:
        sta.active(True)
        sta.connect(ssid, passwd)
        simple_connect()


def simple_update():
    print("Update begin...")
    simple_connect()

    res = urequests.get(SERVER + '/get_update_list')

    if res.status_code == 200 and res.json().get('is_suc'):
        comp_list = res.json().get('data')
        for comp in comp_list:
            res = urequests.get(SERVER + '/update/' + comp)
            if res.status_code == 200 and res.json()['is_suc']:
                data = res.json()['data']
                with open(data['path'], 'w') as fd:
                    fd.write(data['content'])
                    print('[Installing]: ' + data['path'] + ' installed!')
        with open('coll_config.json', 'w') as fd:
            json.dump({
                "role": ROLE,
                "wifi": WIFI_CONFIG,
                "version": VERSION,
                "server": SERVER
            }, fd)
        # Re-create main.py
        print('[Processing]: set core as default module')
        with open('main.py', 'w') as fd:
            fd.write("""from core import *\n""")
        print('[Success]: waiting for reset chip...')
        sleep(3)
        machine.reset()


def install():
    for _file in os.listdir():
        if _file in ['main.py']:
            continue
        os.remove(_file)

    # Create init.py
    with open('main.py', 'r') as main_fd:
        data = main_fd.read()[:-12]
        with open('init.py', 'w') as init_fd:
            print('[Processing]: create init module')
            init_fd.write(data)

    # Re-create main.py
    print('[Processing]: update main module')
    with open('main.py', 'w') as main_fd:
        main_fd.write("""from init import simple_update\nsimple_update()\n""")
    machine.reset()


install()
collector_app.App()
