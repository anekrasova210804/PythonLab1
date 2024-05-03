import abc
import datetime
import random
import time


class Worker(abc.ABC):
    __workerName: str
    __workerShift: int
    __workerCelery: int

    @abc.abstractmethod
    def get_order(self, _order):
        pass

    @abc.abstractmethod
    def get_shift(self, _store_start_shift: datetime.datetime, _store_end_shift: datetime.datetime):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass


class Courier(Worker):
    __inStore: bool
    __storePosition: int
    __time_back: datetime.datetime

    def get_worker_name(self):
        return self.__workerName

    def add_to_celery(self, amount: int):
        self.__workerCelery += amount

    def get_celery(self):
        return self.__workerCelery

    def get_worker_shift(self):
        return self.__workerShift

    def set_store_position(self, _position: int):
        self.__storePosition = _position

    def get_store_position(self):
        return self.__storePosition

    def set_in_store(self, _statement):
        self.__inStore = _statement

    def get_in_store(self):
        return self.__inStore

    def get_time_back(self):
        return self.__time_back

    def __str__(self):
        return self.__workerName + " - Courier"

    def __init__(self, _name, _position):
        self.__workerName = _name
        self.__inStore = False
        self.__storePosition = _position
        self.__time_back = datetime.datetime.now()
        self.__workerCelery = 0

    def get_order(self, _order):
        self.__time_back = \
            (datetime.datetime.now() + datetime.timedelta
                (seconds=2 * self.calculate_delivery_time(_order.get_user_position()) + 4))

        print("Order began being delivered by a Courier " + self.__workerName)
        time.sleep(2)  # вместо мин
        self.set_in_store(False)
        print("Order left Store and is now on its way!")
        _order.set_status("ON ITS WAY")
        time.sleep(self.calculate_delivery_time(_order.get_user_position()))
        print("Order in process of being given to the costumer!")
        time.sleep(2)  # вместо мин

    def get_shift(self, _store_start_shift: datetime.datetime, _store_end_shift: datetime.datetime):
        time_difference = (_store_end_shift - _store_start_shift).total_seconds()
        time_difference //= (60 * 60)
        self.__workerShift = random.randint(1, int(time_difference))

    def calculate_delivery_time(self, _position):
        return 2 * abs(_position - self.get_store_position())  # вместо 30 сек


class Storekeeper(Worker):
    __Available: bool = False

    def get_worker_name(self):
        return self.__workerName

    def add_to_celery(self, amount: int):
        self.__workerCelery += amount

    def get_celery(self):
        return self.__workerCelery

    def set_available(self, _statement):
        self.__Available = _statement

    def get_worker_shift(self):
        return self.__workerShift

    def get_available(self):
        return self.__Available

    def __str__(self):
        return self.__workerName + " - Storekeeper"

    def __init__(self, _name):
        self.__workerName = _name
        self.__workerCelery = 0

    def get_order(self, _order):
        print("Order began being assembled by a Storekeeper " + self.__workerName)
        time.sleep(self.calculate_assembling_time(_order))
        print("Order finished being assembled!")
        _order.set_status("ASSEMBLED")

    @staticmethod
    def calculate_assembling_time(_order):
        result = 0
        for j in _order.get_dict().values():
            result += 3 * j  # вместо 45

        return result

    def get_shift(self, _store_start_shift: datetime.datetime, _store_end_shift: datetime.datetime):
        time_difference = (_store_end_shift - _store_start_shift).total_seconds()
        time_difference //= (60 * 60)
        self.__workerShift = random.randint(1, int(time_difference))
