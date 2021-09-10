import machine
import network
import urequests
from time import sleep
from network import STAT_CONNECTING
from network import STAT_NO_AP_FOUND
from network import STAT_WRONG_PASSWORD
from network import STAT_HANDSHAKE_TIMEOUT

from utils import backup
from utils import init_config


CONFIG = init_config('coll_config.json')


def connect():
    sta = network.WLAN(network.STA_IF)
        
    if sta.status() == STAT_CONNECTING:
        print('[Connecting]: this may take a few seconds...')
        sleep(2)
        return connect()
    elif sta.status() in [STAT_NO_AP_FOUND, STAT_WRONG_PASSWORD]:
        return print('[Fatal error]: ssid not found or password incorrect!')
    elif sta.status() == STAT_HANDSHAKE_TIMEOUT:
        return print('[Error]: timeout!')
    elif sta.isconnected():
        return print('[Success]: Connect Wi-Fi successfully')
    else:
        # Get wifi configuration
        wifi_config = CONFIG['wifi']
        ssid = wifi_config['ssid']
        passwd = wifi_config['passwd']

        sta.active(True)
        sta.connect(ssid, passwd)
        connect()


def update(*comps):
    # Try connect to wifi
    connect()
    server = CONFIG['server']

    # Set default component
    comps = comps or ['core']

    length = str(len(comps))
    failed_lst = []

    for comp_idx, comp in enumerate(comps):
        comp_idx = str(comp_idx + 1)
        print('[' + comp_idx + '/' + length + ']', end='  ')
        res = urequests.get(server + '/update/' + comp)
        json_res = res.json()

        if res.status_code == 200:
            if json_res.get('is_suc'):
                data = json_res['data']
                # Backup old firmware
                if not backup(data['path']):
                    print('[' + comp_idx + '/' + length + ']', end='  ')
                    print('[' + data['path'] + '] will not upgrade')
                    failed_lst.append(comp)
                    continue

                with open(data['path'], 'w') as fd:
                    fd.write(data['content'])
                print('[' + comp_idx + '/' + length + ']', end='  ')
                print('Update [' + data['path'] + '] successfully!')

            else:
                print('Update [' + data['path'] + '] failed. '\
                    'Request Error: ' + json_res.get('msg'))
        else:
            print('Update [' + data['path'] + '] failed. '\
                'HTTP Error: ' + str(res.status_code))
    if str(len(failed_lst)) != length:
        with open('last_change.dat', 'a') as fd:
            fd.write('EOF\n')
        print('Waiting for reset...')
        sleep(2)
        machine.reset()
    else:
        print('Upgrade all failed')
