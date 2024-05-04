import datetime
import random
import time
from collections import Counter

import item
import order
import provider
import worker


class Store:
    __storeItemList: dict = {}
    __storeId: str
    __storeRequest: dict = {}
    __storeAvailableProviders: list[provider.Provider]
    __storePosition: int
    __storeWorkers: list[worker.Worker]
    __storeStartShift: datetime.datetime
    __storeEndShift: datetime.datetime

    def __init__(self, store_id, store_position: int, _start: datetime.datetime, _finish: datetime.datetime,
                 _providers: list):
        self.__storeId = store_id
        self.__storePosition = store_position
        self.__storeStartShift = _start
        self.__storeEndShift = _finish
        self.__storeAvailableProviders = _providers
        self.__storeWorkers = [worker.Courier(store_id + "C", store_position), worker.Storekeeper(store_id + "S")]

    def get_store_start_shift(self):
        return self.__storeStartShift

    def get_store_end_shift(self):
        return self.__storeEndShift

    def get_store_workers(self):
        return self.__storeWorkers

    def show_store_workers(self):
        for i in range(len(self.__storeWorkers)):
            print(str(i + 1) + ". " + str(self.__storeWorkers[i]))

    def get_store_id(self):
        return self.__storeId

    def get_position(self):
        return self.__storePosition

    def show_current_request(self):
        k = 1
        for i, j in self.__storeRequest.items():
            print(str(k), ". ", str(i), ". Asked: ", str(j))
            k += 1

    def get_available_providers(self):
        return self.__storeAvailableProviders

    def show_available_providers(self):
        k = 1
        for i in self.__storeAvailableProviders:
            print(str(k), ". ", str(i))
            k += 1

    def get_store_item_list(self):
        return self.__storeItemList

    def set_store_item_list(self, _new_list):
        self.__storeItemList = _new_list

    def show_item_list(self):
        k = 1
        for i, j in self.__storeItemList.items():
            print(str(k), ". ", str(i), ". In stock: ", str(j))
            k += 1

    def sample_store_item_list(self):
        k = False
        for i in self.__storeAvailableProviders:
            for j in i.get_provider_item_list().keys():
                if k:
                    self.__storeItemList[j] = 5
                else:
                    self.__storeItemList[j] = 0
                    k = True

    def show_item_list_no_stock_info(self):
        k = 1
        for i in self.__storeItemList.keys():
            print(str(k), ". ", str(i))
            k += 1

    def something_is_missing(self, _order: order.Order):
        checker = False
        for i, j in _order.get_dict().items():
            if self.get_store_item_list()[i] == 0:
                _order.get_dict()[i] = 0
                checker = True
        return checker

    def give_celery(self, _time):
        for i in self.__storeWorkers:
            if (isinstance(i, worker.Courier) and i.get_in_store()) or (isinstance(i, worker.Storekeeper)
                                                                        and i.get_available()):
                i.set_celery(int((datetime.datetime.now() - _time).total_seconds() // 60) * 5)
                print(i.get_worker_name(), "'s budget: " + str(i.get_celery()))

    def is_available_to_deliver(self, _order: order.Order):
        if not (self.get_store_start_shift() <= _order.get_creation_time() < self.get_store_end_shift()):
            return False

        for i in self.get_store_workers():
            if isinstance(i, worker.Courier):
                if not i.get_in_store():
                    if random.randint(0, 9) != 1:
                        if datetime.datetime.now() >= i.get_time_back():
                            i.set_in_store(True)
                    else:
                        i.add_to_celery(-300)

        available_workers = False

        for i in self.get_store_workers():
            if isinstance(i, worker.Courier):
                if i.get_in_store():
                    available_workers = True
                    break

        if not available_workers:
            return False
        else:
            available_workers = False

        for i in self.get_store_workers():
            if isinstance(i, worker.Storekeeper):
                if i.get_available():
                    available_workers = True

        if not available_workers:
            return False

        return True

    def calculate_approximate_time(self, _order: order.Order, _place: int):
        result = _order.get_creation_time()
        _order.set_dict({key: val for key, val in _order.get_dict().items() if val != 0})
        for i, j in _order.get_dict().items():
            result += datetime.timedelta(seconds=3 * min(j, self.get_store_item_list()[i]))
        result += datetime.timedelta(seconds=2 * abs(self.__storePosition - _place)) + datetime.timedelta(seconds=4)
        return result

    def update_stocks(self, _item: item.Item, _count: int):
        print("NEW REQUEST CREATED BECAUSE OF LACKING PRODUCT ITEMS!!")
        time.sleep(2*_count)
        needed_index = next((i for i, obj in enumerate(self.get_available_providers()) if obj.get_provider_id()
                             == _item.get_provider_id()))
        self.set_store_item_list(Counter(self.get_store_item_list()) +
                                 Counter(self.__storeAvailableProviders[needed_index].send_order({_item: _count})))

    def take_order(self, _order: order.Order):
        print("The order has started being processed!")
        _order.set_status("ACCEPTED")
        for i in self.get_store_workers():
            if isinstance(i, worker.Courier):
                if i.get_in_store():
                    _order.set_courier(i)
                    break

        for i in self.get_store_workers():
            if isinstance(i, worker.Storekeeper):
                if i.get_available():
                    _order.set_storekeeper(i)
                    break

        for i, j in _order.get_dict().items():
            _order.get_dict()[i] = min(j, self.get_store_item_list()[i])
            self.__storeItemList[i] -= _order.get_dict()[i]

        _order.set_dict({key: val for key, val in _order.get_dict().items() if val != 0})
        if bool(_order.get_dict()):
            _order.get_storekeeper().get_order(_order)
            _order.get_courier().get_order(_order)

    def __create_request(self, _provider: provider.Provider):
        if not self.__storeItemList:
            print("Store has nothing in stock at the moment.")

        print("\tProduct available from Provider", _provider.get_provider_id())
        _provider.show_provider_item_list()
        self.__storeRequest = {}
        if not _provider.get_provider_item_list():
            print("Sadly, provider has nothing available at the moment.")
        else:
            while True:
                print("\nDo you want to request more products? (Yes or Other)")
                if input().lower() == "yes":
                    product_index = int(input("Please write the index of a product you wish to request: "))

                    while product_index > len(list(_provider.get_provider_item_list())):
                        print("Incorrect index!!")
                        product_index = int(input("Please write the index of a product you wish to request: "))

                    product_count = int(input("Please write the amount of a product you wish to request: "))

                    while product_count < 0:
                        print("Incorrect amount!!")
                        product_index = int(input("Please write the amount of a product you wish to request: "))

                    self.__storeRequest[list(_provider.get_provider_item_list())[product_index - 1]] = product_count
                else:
                    break

        if self.__storeRequest:
            for i in _provider.get_provider_item_list().keys():
                if i not in list(self.__storeRequest.keys()):
                    self.__storeRequest[i] = 0

            print("\tCongrats! The request has been created:")
            for i in self.__storeRequest.keys():
                i.set_provider_id(_provider.get_provider_id())
            self.show_current_request()

    def send_request(self):
        print("\nYou are creating a request for a Store: " + self.__storeId + "\n")
        for i in self.__storeAvailableProviders:
            self.__create_request(i)
            if self.__storeRequest:
                self.set_store_item_list(Counter(self.get_store_item_list()) +
                                         Counter(i.send_order(self.__storeRequest)))
                print("Request has been properly processed.")

    def start_shift(self):
        self.add_workers()
        for i in self.__storeWorkers:
            i.get_shift(self.__storeStartShift, self.__storeEndShift)
            if isinstance(i, worker.Storekeeper):
                i.set_available(True)
            if isinstance(i, worker.Courier):
                i.set_in_store(True)
        self.send_request()

    def add_a_worker(self, _name: str, are_they_a_storekeeper: bool):
        if are_they_a_storekeeper:
            self.__storeWorkers.append(worker.Storekeeper(_name))
        else:
            self.__storeWorkers.append(worker.Courier(_name, self.__storePosition))

    def add_workers(self):
        if not self.__storeWorkers:
            print("It seems ", self.__storeId, " has no workers. You will need to add at least one courier and"
                                               " storekeeper!")

            self.add_a_worker(input("Write the name of a courier: "), False)
            self.add_a_worker(input("Write the name of a storekeeper: "), True)
        else:
            print("\n" + self.__storeId + "'s workers: ")
            self.show_store_workers()

            if not any(isinstance(x, worker.Courier) for x in self.get_store_workers()):
                self.add_a_worker(input("You will need a Courier. Write the name of a courier: "), False)
            if not any(isinstance(x, worker.Storekeeper) for x in self.get_store_workers()):
                self.add_a_worker(input("You will need a Storekeeper. Write the name of a storekeeper: "), True)

        while True:
            print("\nDo you want to add another worker? (Yes or Other)")
            if input().lower() == "yes":
                if_storekeeper = input("Write YES, if a worker is a storekeeper or something else, if "
                                       "they are a courier: ")
                self.add_a_worker(input("Please write the name of a worker: "), if_storekeeper.lower() == "yes")
            else:
                break
