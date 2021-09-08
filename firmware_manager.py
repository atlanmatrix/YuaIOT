import json
import machine
import network
import urequests

from time import sleep


FM_VERSION = '0.0.3'


def connect():
    ssid = 'Xiaomi_CCD8'
    passwd = 'Mxsoft@806'
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(ssid, passwd)


def update(comp='main'):
    res = urequests.get('http://192.168.31.54:8899/update/' + comp)
    print(res.json)
    print(res.status_code)
    print(dir(res))
    json_res = json.loads(res.text)
    if json_res.get('is_suc'):
        data = json_res['data']
        f = open(data['path'], 'w')
        f.write(data['content'])
        f.close()
        print('Update ' + data['path'] + ' successfully!')
        print('Waiting for reset...')
        sleep(2)
        machine.reset()


def backup_firmware():
    pass


def restore_firmware():
    pass


connect()
