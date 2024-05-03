from dataclasses import dataclass


@dataclass
class Item:
    __itemProviderId: str
    __itemName: str
    __itemPrice: int

    def __init__(self, _name: str, _price: int):
        self.__itemName = _name
        self.__itemPrice = _price
        self.__itemProviderId = ""

    def __str__(self):
        return ("Product: " + self.__itemName + ". Price: " + str(
            self.__itemPrice) + ". Provider: " + self.__itemProviderId)

    def __eq__(self, other):
        if isinstance(other, Item):
            return ((self.__itemProviderId, self.__itemName, self.__itemPrice) ==
                    (other.__itemProviderId, other.__itemName, other.__itemPrice))
        return False

    def __hash__(self):
        return hash((self.__itemProviderId, self.__itemName, self.__itemPrice))

    def get_price(self):
        return self.__itemPrice

    def get_provider_id(self):
        return self.__itemProviderId

    def get_name(self):
        return self.__itemName

    def set_price(self, _price):
        self.__itemPrice = _price

    def set_provider_id(self, _provider_id):
        self.__itemProviderId = _provider_id

    def set_name(self, _item_name):
        self.__itemName = _item_name
