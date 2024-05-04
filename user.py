import datetime

import order
import store


class User:
    __userName: str
    __userAddress: int = 0
    __availableStores: list[store.Store]
    __userOrder: order.Order

    def __init__(self, _stores: list[store.Store]):
        self.__availableStores = _stores
        self.__userOrder = order.Order()

    def get_available_stores(self):
        return self.__availableStores

    def register(self):
        print("\tStart of a registration!")
        self.__userName = input("Please write your name: ")
        _user_address = int(input("Please write your address: "))
        while 0 > _user_address or _user_address > 100:
            print("Incorrect address!")
            _user_address = int(input("Please write your address again: "))
        self.__userAddress = _user_address

    def make_order(self):
        print("\n\tYou are now creating an Order!")
        self.__userOrder.set_status("CREATED")
        self.__userOrder.set_dict({})
        self.__userOrder.set_user_position(self.__userAddress)
        min_store = self.__availableStores[0]
        min_store.show_item_list_no_stock_info()

        while True:
            print("\nDo you want to add a new product to your Order? (Yes or Other)")
            if input().lower() == "yes":
                _index = int(input("Please write the index of a product you wish to buy: "))
                while _index > len(list(min_store.get_store_item_list())) or _index < 0:
                    print("Incorrect index!")
                    _index = int(input("Please write your index again: "))

                _count = int(input("Please write the amount of a product you wish to buy: "))
                while _count < 0:
                    print("Incorrect amount!")
                    _count = int(input("Please write amount again: "))
                _item = list(min_store.get_store_item_list())[_index - 1]
                self.__userOrder.get_dict()[_item] = _count
            else:
                break

        self.__userOrder.set_creation_time(datetime.datetime.now())

        availability_check = False
        comparison_list = []
        for i in range(len(self.__availableStores)):
            comparison_list.append((self.__availableStores[i].is_available_to_deliver(self.__userOrder),
                                    self.__availableStores[i].calculate_approximate_time(self.__userOrder,
                                                                                         self.__userAddress)))
            if comparison_list[i][0]:
                availability_check = True
                if comparison_list[i][1] < min_store.calculate_approximate_time(self.__userOrder, self.__userAddress):
                    min_store = self.get_available_stores()[i]

        if bool(self.__userOrder.get_dict()):
            if availability_check:
                print("\nThe store that is optimal for you is ", min_store.get_store_id())
                cancelled_checker = ""
                if min_store.something_is_missing(self.__userOrder):
                    print("\nIt appears as if some products ar missing in this store. "
                          "Do you want to cancel your order?")
                    cancelled_checker = input("Please write \"yes\" if you want to cancel your order: ")

                if cancelled_checker.lower() == "yes":
                    print("We are deeply sorry.... :(")
                else:
                    self.__userOrder.set_creation_time(datetime.datetime.now())
                    print("Your TOTAL: " + str(self.__userOrder.calculate_total_price()) + "\n")
                    if {key: val for key, val in self.__userOrder.get_dict().items() if val != 0}:
                        print("The APPROXIMATE time of delivery is ",
                              str(min_store.calculate_approximate_time(self.__userOrder, self.__userAddress)), "\n")
                    self.take_order(min_store)  # взяли вещи
            else:
                print("I'm sorry, no stores are available at the moment!")

    def take_order(self, _store: store.Store):
        if {key: val for key, val in self.__userOrder.get_dict().items() if val != 0}:
            _store.take_order(self.__userOrder)
            self.__userOrder.set_status("DELIVERED")
            self.__userOrder.set_delivery_time(datetime.datetime.now())
            print("Order has been delivered at time ", self.__userOrder.get_delivery_time(), "!!!!\n")
            print("\tYour order:\n", str(self.__userOrder))

        if _store.something_is_missing(self.__userOrder):
            for i in self.__userOrder.get_dict().keys():
                if _store.get_store_item_list().get(i) == 0:
                    _store.update_stocks(i, 5)
