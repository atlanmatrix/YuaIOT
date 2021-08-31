import os
import json
import datetime
from time import time
from collections import defaultdict

from typing import Any
from tornado import httputil
import tornado.ioloop
import tornado.web


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


def make_app():
    return tornado.web.Application([
        (r"/register", DeviceRegisterHandler),
        (r"/devices", DeviceDataHandler),
        (r"/destroy", DeviceDestroyHandler),
    ])


def init_sys():
    """
    Init IOT server configuration
    :return:
    """
    pass


if __name__ == "__main__":
    app = make_app()
    app.listen(8899)
    tornado.ioloop.IOLoop.current().start()
