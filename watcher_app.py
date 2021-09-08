import os
import json
import datetime
import logging
from time import time
from collections import defaultdict

from typing import Any
from tornado import httputil
import tornado.ioloop
import tornado.web

from utils import get_file_size


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application: "tornado.web.Application", 
                 request: httputil.HTTPServerRequest, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)


class DeviceRegisterHandler(BaseHandler):
    """
    Register device
    """
    def get(self):
        # Register status query
        pass

    def post(self):
        # Create register record with device's information
        pass


class DeviceDestroyHandler(BaseHandler):
    """
    Destroy device
    """
    def get(self):
        pass

    def post(self):
        pass


class DeviceDataHandler(BaseHandler):
    """
    Get registered device infos,
    such as Watchers' ips etc.
    """
    def get(self):
        # role = self.get_argument("role")
        # if role is None:
        #     return self.write({"is_suc": False, "error": "Invalid Role"})

        now = int(time.time())
        # TODO 
        # switch to influxDB and MongoDB here.
        DEVICES_INFO_FILE = r"./devices.json"

        # No device has registered
        if not os.path.exists(DEVICES_INFO_FILE):
            return self.write({"is_suc": True, "data": {}})
        
        with open(DEVICES_INFO_FILE, "r") as fd:
            # [{}, {}, {}]
            devices = json.load(fd)
        
        # Get online devices
        # if check_time before 5s, this device maybe offline
        online_devices = defaultdict(list)
        for device in devices:
            # {'uid': '', 'name': '', 'check_time': '', 'IP': '', 'role': '', 'group': ''}
            if now - int(device.get("check_time", 0)) < 5:
                online_devices[device.get("role")].append(device.get("IP"))

        return online_devices


    def post(self):
        pass


class ServerIPHandler(BaseHandler):
    def get(self):
        data = {}
        with open("./server.json", "r") as fd:
            data = json.load(fd)
        
        position = self.get_argument("po")
        ip = data.get(position)
        return self.write(ip)

    def post(self):
        pass


class HeartbeatHandler(BaseHandler):
    """
    Get IOT device status
    """
    def get(self):
        device_sn = self.get_argument("sn")
        with open("./hearbeat.log", "a") as fd:
            fd.write(
                f"{str(datetime.datetime.now())[:19]}"
                f"  {device_sn}"
                f"  {self.request.remote_ip}"
                f"\n")
        return self.write("ok")


class UpdateCollectorHandler(BaseHandler):
    """
    Update fixture for ESP32 chip
    """
    def get(self):
        # Get client version
        client_v = self.get_argument('v')

        # Primary process
        from collector_app import App
        app = App()
        server_v = app.version()
        client_v_lst = client_v.split(".")
        server_v_lst = server_v.split(".")

        # Check if local version is newest
        is_newest = True
        for i in range(3):
            if client_v_lst[i] < server_v_lst[i]:
                is_newest = False
                break

        if is_newest:
            return self.write({
                "is_suc": True,
                "data": {"is_newest": True}
            })
        else:
            return self.write({
                "is_suc": True,
                "data": {
                    "is_newest": False, 
                    "ver": server_v, 
                    "size": get_file_size("./collector_app")
                }
            })


class FirmwareHandler(BaseHandler):
    def get(self, comp):
        # Map of comps and files
        firmware_comps = {
            'main': 'main.py',
            'fm': 'firmware_manager.py',
            'inspector': 'inspector.py',
            'middle': 'middle_man.py'
        }

        file_path = firmware_comps.get(comp) or 'main.py'
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r') as fd:
                content = fd.read()
            return self.write({'is_suc': True, 'data': {
                'content': content,
                'path': file_path
            }})
        return self.write({'is_suc': False, 'msg': ''})


def make_app():
    return tornado.web.Application([
        (r"/register", DeviceRegisterHandler),
        (r"/devices", DeviceDataHandler),
        (r"/destroy", DeviceDestroyHandler),
        (r"/check_for_update", UpdateCollectorHandler),
        (r"/update/(.*)", FirmwareHandler),
    ])


def init_sys():
    """
    Init IOT server configuration
    :return:
    """
    pass


if __name__ == "__main__":
    app = make_app()
    port = 8899
    app.listen(port)
    print('Listening on ' + str(port))
    logging.info('Listening on ' + str(port))
    tornado.ioloop.IOLoop.current().start()
