# -*- coding: utf_8 -*-
# @Author : Claude Manchester
# @Time : 2021/07/02 13:54
# @Remark : Ice box manage
import json

from handlers.yua_sys import BaseHandler
from dao.tool import ice_box_dao


class IceBoxHandler(BaseHandler):
    def post(self):
        result = ice_box_dao.db_list_food(self.db)
        return self.write({"is_suc": True, "msg": result})

    def get(self):
        op_type = self.get_argument("op")
        if op_type == "get":
            result = ice_box_dao.db_list_food(self.db)
            return self.write(json.dumps({"is_suc": True, "msg": list(result)},
                                         ensure_ascii=False))
        elif op_type == "inc":
            name = self.get_argument("name")
            quantity = self.get_argument("quantity")
            result = ice_box_dao.db_increase_food(self.db, name, quantity)
            # result = self.increase_food(name, quantity)
            if result:
                return self.write(
                    {"is_suc": True, "msg": "Increase successfully!"})
            else:
                return self.write({"is_suc": False, "msg": "Increase failed!"})
        elif op_type == "dec":
            pass
        else:
            return self.write({"is_suc": False, "msg": "Invalid Operation!"})
