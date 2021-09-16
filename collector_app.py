import os
import usocket as socket
import network
import urequests
import ure as re


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
        # self._get_sys_status()
        # Create access point
        self._create_ap()
        # Provide web service
        self._run_web_server()

    def _random_hex_str(self, len=4):
        hex_str = ''.join(
            [('0' + hex(ord(os.urandom(1)))[2:])[-2:] for _ in range(len // 2)])
        return hex_str

    def _random_essid(self):
        return 'ESP32_' + self._random_hex_str(4)

    def _init_config(self):
        # If config file not found, create one from default(TODO)
        # Else read config(TODO)
        if not 'coll_config.py' in os.listdir():
            # if not os.path.exists('coll_config.py'):
            # if 'ap' not in self._config:
            self._config['ap'] = {'essid': self._random_essid()}
            # if 'server' not in self._config:
            self._config['server'] = 'iot.yua.im'
        else:
            pass
        print("_init_config:%s" % str(self._config))

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
        sta_status = self._sta.ifconfig()

        status.update(flash_status)
        return status

    def _create_ap(self):
        # Create access point for connection
        try:
            ap_config = self._config['ap']
            self._ap.config(essid=ap_config['essid'])
            self._ap.active(True)
            print("set ap " + ap_config['essid'])
        except Exception as e:
            print('_create_ap:%s' % e)
            pass

    def _default_handler(self):
        pass

    def _request_handler(self, method, path):
        # Only HTTP 'get' method supported now
        # TODO
        if method.find('GET') >= 0:
            if path.find('/get_wifi_html') >= 0:
                self._default_handler()
                html = """
                <form>
                    ssid:<input type="text" id="ssid" >
                    <br>
                    password:<input type="text" id="password" >
                    <br><br>
                    <input type="submit" value="submit" onclick="submitInfo()">
                </form> 
                <script>
                    function submitInfo(){
                        var ssid = document.getElementById("ssid").value;
                        var password = document.getElementById("password").value;
                        window.location.href = 'set_wifi?ssid='+ssid+'&password='+password;
                    }
                </script>
                """
                return self._html.replace('$$', html)
            elif path.find('/set_wifi') >= 0:
                """
                path = '/set_wifi?ssid=qvb&password=1234'
                ['/set_wifi', 'ssid', 'qvb', 'password', '1234']
                """
                data = re.compile(r'[?&=]').split(path)
                self._default_handler()
                self._config['wifi'] = {
                    'ssid': data[2],
                    'passwd': data[4]
                }
                self._set_sta()
                return self._html.replace('$$', '<h1>success!</h1>')
            else:
                # self._default_handler()
                return None
        else:
            # self._default_handler()
            return None

    def _run_web_server(self):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(addr)
        server.listen(5)
        print('listening on', addr)

        while True:
            cl, addr = server.accept()
            print('client connected from', addr)
            try:
                data = cl.recv(1024)
                method = data.split(b' ')[0].decode("utf-8")
                path = data.split(b' ')[1].decode("utf-8")

                print(method, path)
                response = self._request_handler(method, path)
                if response:
                    cl.send(b'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                    cl.send(bytes(response.encode('utf-8')))
                    cl.settimeout(10)
            except Exception as e:
                print('_run_web_server:%s' % e)
            cl.close()

    def _get_ap_lst(self):
        ap_lst = self._sta.scan()
        return ap_lst

    def _set_sta(self):
        try:
            self._sta.active(True)
            wifi_conf = self._config['wifi']
            print("config:", self._config)
            count = 0
            while not self._sta.isconnected() and count < 3:
                self._sta.connect(wifi_conf['ssid'], wifi_conf['passwd'])
                count += 1
            print('network config:', self._sta.ifconfig())
        except Exception as e:
            print('_set_sta:%s' % e)
            pass

    def _update_firmware(self):
        # Update firmware from cloud server  
        if self._sta is not None and self._server is not None:
            res = urequests.get(self._server + '/check_for_update?v=' + self._version)
            # TODO: result handler here
            pass


if __name__ == "__main__":
    app = App()
