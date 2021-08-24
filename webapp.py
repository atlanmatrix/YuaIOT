import json

from typing import Any
from tornado import httputil
import tornado.ioloop
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application: "tornado.web.Application", 
                 request: httputil.HTTPServerRequest, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)


class DeviceMonitor(BaseHandler):
    def get(self):
        data = {}
        with open("./server.json", "r") as fd:
            data = json.load(fd)
        
        position = self.get_argument("po")
        ip = data.get(position)
        return self.write(ip)

    def post(self):
        pass


class ServerIPHandler(BaseHandler):
    def get(self):
        pass

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
        pass


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


def make_app():
    return tornado.web.Application([
        (r"/health", HealthHandler),
        (r"/register", RegisterHandler),
        (r"/destroy", DestroyHandler),
        (r"/heartbeat", HeartbeatHandler),
        (r"/task", TaskDistributionHandler),
    ])


def init_sys():
    """
    Init IOT server configuration
    :return:
    """
    pass


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
