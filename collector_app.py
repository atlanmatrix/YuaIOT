import os
import socket
import network
import urequests


class App:
    def __init__(self):
        self._html = """<!DOCTYPE html>
            <html>
                <head> <title>ESP32 Web Server</title> </head>
                <body>$$</body>
            </html>
        """

        self._version = '0.0.1'
        self._ap = network.WLAN(network.AP_IF)
        self._sta = network.WLAN(network.STA_IF)
        self._config = {
            'role': 2,
            'wifi': None
        }

        self._status = {}

        # Init configurations
        self._init_config()
        # Get system status
        self._get_sys_status()
        # Create access point
        self._create_ap()
        # Provide web service
        self._run_web_server()

    def _random_hex_str(self, len):
        hex_str = ''.join(
            [('0'+hex(ord(os.urandom(1)))[2:])[-2:] for _ in range(len // 2)])
        return hex_str

    def _random_essid(self):
        return 'ESP32_' + self._random_hex_str()
        
    def _init_config(self):
        # If config file not found, create one from default(TODO)
        # Else read config(TODO)
        if not os.path.exists('coll_config.py'):
            if 'ap' not in self._config:
                self._config['ap'] = {'essid': self._random_essid()}
            if 'server' not in self._config:
                self._config['server'] = 'iot.yua.im'
        else:
            pass

    def _get_sys_status(self):
        status = {}
        # Get flash status
        statvfs_fields = ['bsize', 'frsize', 'blocks',
                      'bfree', 'bavail', 'files', 'ffree', ]
        flash_status = dict(zip(statvfs_fields, os.statvfs('/')))
        # TODO: Get memory status
        pass
        # TODO: Get connection status
        ap_status = self._ap.ifconfig()
        sta_status = self._sta.config()

        status.update(flash_status)
        return status

    def _create_ap(self):
        # Create access point for connection
        try:
            ap_config = self._config.ap
            self._ap.config(essid=ap_config['essid'])
            self._ap.active(True)
        except:
            pass

    def _default_handler(self):
        pass

    def _request_handler(self, method, path):
        # Only HTTP 'get' method supported now
        # TODO
        if method == 'get':
            if path == '/':
                self._default_handler()
            else:
                self._default_handler()
        else:
            self._default_handler()

    def _run_web_server(self):
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
                if not line or line == b'\r\n':
                    break
                line_no += 1
            self._request_handler(method, path)

            response = self._html.replace('$$', '<h1>Hello world!</h1>')
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()

    def _get_ap_lst(self):
        ap_lst = self._sta.scan()
        return ap_lst

    def _set_sta(self):
        try:
            self._sta.active(True)
            wifi_conf = self._config['wifi']

            count = 0
            while not self._sta.isconnected() and count < 3:
                self._sta.connect(wifi_conf['ssid'], wifi_conf['passwd'])
                count += 1
        except:
            pass

    def _update_firmware(self):
        # Update firmware from cloud server
        if self._sta is not None and self._server is not None:
            res = urequests.get(self._server + '/check_for_update?v=' + self._version)
            # TODO: result handler here
            pass

if __name__ == "__main__":
    app = App()
