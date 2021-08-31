import os
import socket
import network
import urequests


ROLE = 'collector'
VERSION = '0.0.1'


html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Web Server</title> </head>
    <body> <h1>Nothing here</h1>
    </body>
</html>
"""

ap = None
sta = None
# Official Server
server = 'http://yua.im:8899'


def get_flash_status():
    statvfs_fields = ['bsize', 'frsize', 'blocks',
                      'bfree', 'bavail', 'files', 'ffree', ]
    result = dict(zip(statvfs_fields, os.statvfs('/')))
    return result


def create_ap():
    global ap
    essid = 'ESP32_' + \
        ''.join([('0'+hex(ord(os.urandom(1)))[2:])[-2:] for _ in range(2)])
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=essid)
    ap.active(True)


def set_wifi():
    pass


def set_processor():
    pass


def set_watcher():
    pass


def default_handler():
    """
    Display status of ESP32 chip
    """
    pass


def auto_update():
    # Update fixture from cloud server
    if sta is not None and server is not None:
        res = urequests.get(server + '/check_for_update?v=' + VERSION)
        # result handler here
        pass


def request_handler(method, path):
    # Only HTTP 'get' method supported now
    if method == 'get':
        if path == '/':
            set_wifi()
        elif path == '/watcher':
            set_watcher()
        else:
            default_handler()
    else:
        default_handler()


def create_web_server():
    global server
    addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(5)
    print('listening on', addr)

    while True:
        cl, addr = server.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        line_no = 0
        method = None
        path = None
        while True:
            line = cl_file.readline()
            if line_no == 0:
                method = line.split(b' ')[0]
                path = line.split(b' ')[1]
            print(line)
            if not line or line == b'\r\n':
                break
            line_no += 1
        request_handler(method, path)

        print(f'addr')
        response = html
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()


create_ap()
create_web_server()


# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.scan()
# while not wlan.isconnected():
#     wlan.connect('aizizhudeiwifi', 'YDRBxERmW43sgNIaqMaA8ESuqJt14DS3Gk3OQAINNpepBZpHcgSEn73oMaz10nW')

# ret = urequests.get('http://192.168.0.104:8888/health')
