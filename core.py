import network

from firmware_manager import update
from alias import *
from utils import random_hex_str


VERSION = '0.0.1.0909'
ap = None


def create_ap():
    # Create access point for connection
    global ap
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    try:
        ap_config = {'essid': 'ESP32_' + random_hex_str}
        ap.config(essid=ap_config['essid'])
        ap.active(True)
        with open('apconfig.dat', 'w') as fd:
            fd.write(str(ap.config()))
    except:
        pass

create_ap()
