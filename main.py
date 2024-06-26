import datetime

import item
import provider
import store
import user

item11 = item.Item("Sith Luke Funko Pop", 1000)
item12 = item.Item("Sith Leia Funko Pop", 1200)
item21 = item.Item("Obi-Wan Stickers", 200)
item22 = item.Item("Anakin Stickers", 150)
item23 = item.Item("Ashoka Stickers", 250)
item31 = item.Item("Vader's lightsaber", 8000)

provider1 = provider.Provider("1", {item11: 6, item12: 7})
provider2 = provider.Provider("2", {item21: 24, item22: 22, item23: 12})
provider3 = provider.Provider("3", {item31: 3})

t1 = datetime.time(7, 0, 0)
t2 = datetime.time(23, 0, 0)
t3 = datetime.time(23, 0, 0)

store1 = (store.Store("a", 0, datetime.datetime.combine(datetime.date.today(), t1),
                      datetime.datetime.combine(datetime.date.today(), t2), [provider1, provider2, provider3]))

store2 = (store.Store("b", 100, datetime.datetime.combine(datetime.date.today(), t1),
                      datetime.datetime.combine(datetime.date.today(), t3), [provider1, provider2, provider3]))

store1.sample_store_item_list()
store2.sample_store_item_list()

example_user = user.User([store1, store2])

for i in example_user.get_available_stores():
    i.start_shift()

comp_time = datetime.datetime.now()

while True:
    print("\nDo you want to make new order? (Yes or Other)")
    if input().lower() == "yes":
        example_user.register()

        example_user.make_order()

        print("\tWORKER CELERY:")
        store1.give_celery(comp_time)
        store2.give_celery(comp_time)
    else:
        break
