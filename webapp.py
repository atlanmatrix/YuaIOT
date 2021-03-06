import os
import json
import time
import datetime

from typing import Any
from tornado import httputil
import tornado.ioloop
import tornado.web


def get_file_size(file_path):
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    else:
        return 0


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application: "tornado.web.Application", 
                 request: httputil.HTTPServerRequest, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)


class DeviceMonitor(BaseHandler):
    def get(self):
        pass

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


class HealthHandler(BaseHandler):
    """
    Tell IOT device server status
    """
    def get(self):
        print(f"Device: {self.request.remote_ip} is online")
        return self.write("OK")
        
    def post(self):
        print(f"Device: {self.request.remote_ip} is online")
        return self.write("OK")


class RegisterHandler(BaseHandler):
    """
    Register IOT device
    """
    def get(self):
        pass


class DestroyHandler(BaseHandler):
    """
    Destroy IOT device
    """
    def get(self):
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


class TaskDistributionHandler(BaseHandler):
    """
    Distribute task to IOT device
    """
    def get(self):
        pass


class DeviceDataHandler(BaseHandler):
    """
    Handler
    """
    pass


class UpdateCollectorHandler(BaseHandler):
    """
    Update fixture for ESP32 chip
    """
    def get(self):
        # Get client version
        client_v = self.get_argument('v')

        # Primary process
        from collector_app import VERSION as server_v
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


class RegistrationHandler(BaseHandler):
    """
    Registration of daily task,
    such as reading, playing, watching etc.
    """
    def get(self):
        # Preset dict
        OP_DICT = {
            "01": "Relax Alone",
            "11": "Relax Together",
            "12": "Hard Entertainment",
            "13": "Study",
            "14": "Wash",
            "15": "Before Sleep Relax",
            "16": "Sleep"
        }

        ROLE_DICT = {
            "0": "Pretty",
            "1": "Handsome"
        }

        STATUS_DICT = {
            "0": "Start",
            "1": "End",
            "2": "Pause",
            "3": "Resume"
        }

        EXPECT_LEN = 4

        # Parameters check
        seq = self.get_argument("seq")
        if len(seq) != EXPECT_LEN:
            return self.write("???????????????")

        op = OP_DICT.get(seq[0] + seq[1])
        role = ROLE_DICT.get(seq[2])
        status = STATUS_DICT.get(seq[3])

        if op is None or role is None or status is None:
            return self.write("?????????????????????")

        # Create log dir
        LOG_PATH = "./.log/registration/"
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)

        # Record log
        ts = int(time.time())
        date = str(datetime.datetime.today())[:10]
        with open(rf"./.log/registration/{date}.log", "a") as fd:
            fd.write(f"{ts} {op} {role} {status}")
        return self.write("????????????")

    def post(self):
        pass


def make_app():
    return tornado.web.Application([
        (r"/health", HealthHandler),
        (r"/register", RegisterHandler),
        (r"/destroy", DestroyHandler),
        (r"/heartbeat", HeartbeatHandler),
        (r"/task", TaskDistributionHandler),
        (r"/get_server_ip", ServerIPHandler),
        (r"/registration", RegistrationHandler),
        (r"/check_for_update", UpdateCollectorHandler),
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
