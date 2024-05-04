import item


class Provider:
    __providerItemList: dict
    __providerId: str

    def __init__(self, provider_id, _item_list):
        self.__providerId = provider_id
        self.__providerItemList = _item_list
        for i in self.__providerItemList.keys():
            i.set_provider_id(self.__providerId)

    def __str__(self):
        return self.__providerId + " - Provider"

    def get_provider_id(self):
        return self.__providerId

    def get_provider_item_list(self):
        return self.__providerItemList

    def set_provider_item_list(self, _item_list):
        for i in _item_list.keys():
            i.set_provider_id(self.__providerId)
        self.__providerItemList = _item_list

    def show_provider_item_list(self):
        k = 1
        for i, j in self.get_provider_item_list().items():
            print(str(k), ". ", str(i), ". Available: ", str(j))
            k += 1

    def add_item(self, _item: item.Item, _count):
        _item.set_provider_id(self.__providerId)
        self.__providerItemList[_item] = _count

    def send_order(self, _request):
        print("Request accepted by Provider ", self.__providerId)
        result = self.update_stocks(_request)
        if not result:
            print("Something went wrong. Request FAILED.")
        return result

    def update_stocks(self, _request: dict):
        d, d1 = {}, {}
        for i, j in self.get_provider_item_list().items():
            a = j
            b = _request.get(i, 0)
            d[i] = min(a, b)
            d1[i] = a - d[i]

        self.set_provider_item_list(d1)
        print("Stocks updated.")
        return d
