import os
import json
import network


def random_hex_str(len):
    hex_str = ''.join(
        [('0'+hex(ord(os.urandom(1)))[2:])[-2:] for _ in range(len // 2)])
    return hex_str


def is_file_in_current_dir(file_name):
    all_files = os.listdir()
    return file_name in all_files


def get_entire_html(block):
    tpml = """
        <!DOCTYPE html>
        <html>
            <head> <title>ESP32 Web Server</title> </head>
            <body>$$</body>
        </html>
    """

    html = tpml.replace('$$', block)
    return html


def is_wifi_connected():
    status, _ = sta_ifconfig()
    return status


def is_ap_created():
    status, _ = ap_ifconfig()
    return status


def sta_ifconfig():
    sta = network.WLAN(network.STA_IF)
    if sta.active() and sta.isconnected():
        sta_ifconfig = sta.ifconfig()
        print(sta_ifconfig)
        return True, sta_ifconfig

    print('Not connected')
    return None, None


def ap_ifconfig():
    ap = network.WLAN(network.AP_IF)
    if ap.active():
        ap_ifconfig = ap.ifconfig()
        print(ap_ifconfig)
        print('Isconnected:' + str(ap.isconnected()))
        return True, ap_ifconfig

    print('AP not actived')
    return None, None


def init_config(conf_file):
    try:
        with open(conf_file, 'r') as fd:
            config = json.load(fd)
            return config
    except:
        return None


def copy_file(raw_path, new_path):
    try:
        all_files = os.listdir()
        if raw_path in all_files:
            with open(raw_path, 'r') as fd:
                data = fd.read()
            with open(new_path, 'w') as fd:
                fd.write(data)
            return True, 'Copied'
        else:
            return False, 'Raw file not found'
    except:
        return False, 'Failed'


def backup(raw_path):
    res, msg = copy_file(raw_path, raw_path + '.bak')
    if res or (not res and msg != 'Failed'):
        if res:
            with open('last_change.dat', 'a') as fd:
                fd.write(raw_path + '.bak\n')
        print('Back up [' + raw_path + '] successfully!')
        return True
    else:
        print('Back up [' + raw_path + '] failed.')
        return False


def restore(bak_path):
    copy_file(bak_path[:-4], bak_path)


def roll_back():
    """
    Roll back last changed files
    """
    with open('last_change.dat', 'r') as fd:
        sections = fd.read().split('\nEOF\n')
        if len(sections) > 0:
            section = sections[:-1]
            changes = section.split('\n')
        else:
            changes = []

    length = str(len(changes))
    for change_idx, change in enumerate(changes):
        change_idx = str(change_idx)
        print('[' + change_idx + '/' + length + ']  ' +
              'Start roll back: ' + change)
        restore(change)
        print('[' + change_idx + '/' + length + ']  ' +
              'Roll back: ' + change + ' successfully!')
