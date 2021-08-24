"""
Copyright © 2017-2021 Yua.Im
"""
from abc import ABC
import tornado


class BaseHandler(tornado.web.RequestHandler, ABC):
    """
    System base handler
    """
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.xsrf_token

    @property
    def db(self):
        return self.application.db

    @property
    def env(self):
        return self.application.env

    def get_current_user(self):
        session_id = self.get_secure_cookie("sid")

        if not session_id:
            return None

        result, info = yua_mongo.query_session(session_id)

        return info if result else None
