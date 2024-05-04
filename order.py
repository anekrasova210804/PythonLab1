import datetime
from dataclasses import dataclass

import item
import worker


@dataclass
class Order:
    __userPosition: int
    __orderStatus: str
    __orderDict: {item.Item, int}
    __orderCreationTime: datetime.datetime
    __orderDeliveryTime: datetime.datetime
    __orderStorekeeper: worker.Storekeeper = None
    __orderCourier: worker.Courier = None

    def __init__(self):
        self.__userPosition = 0
        self.__orderStatus = "EMPTY"
        self.__orderDict = {}
        self.__orderCreationTime = datetime.datetime.now()
        self.__orderDeliveryTime = datetime.datetime.now()

    def __str__(self):
        result = ""
        k = 1
        for i, j in self.__orderDict.items():
            result += str(k) + ". " + str(i) + " ORDERED: " + str(j) + "\n"
            k += 1
        return result

    def set_user_position(self, _position: int):
        self.__userPosition = _position

    def get_user_position(self):
        return self.__userPosition

    def set_status(self, _status: str):
        self.__orderStatus = _status

    def get_status(self):
        return self.__orderStatus

    def get_dict(self):
        return self.__orderDict

    def set_dict(self, _dict: dict):
        self.__orderDict = _dict

    def get_creation_time(self):
        return self.__orderCreationTime

    def set_creation_time(self, _creation: datetime.datetime):
        self.__orderCreationTime = _creation

    def get_delivery_time(self):
        return self.__orderDeliveryTime

    def set_delivery_time(self, _delivery: datetime.datetime):
        self.__orderDeliveryTime = _delivery

    def get_storekeeper(self):
        return self.__orderStorekeeper

    def set_storekeeper(self, _storekeeper: worker.Storekeeper):
        self.__orderStorekeeper = _storekeeper

    def get_courier(self):
        return self.__orderCourier

    def set_courier(self, _courier: worker.Courier):
        self.__orderCourier = _courier

    def calculate_total_price(self):
        result = 0
        for i, j in self.__orderDict.items():
            result += i.get_price()*j
        return result
