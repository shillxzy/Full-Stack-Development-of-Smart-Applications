"""Завдання 8 a-e. Демонстрація класів Shop і Discount."""
from shop import Discount, Shop

print("--- a ---")
store = Shop("Rozetka", "електроніка")
print("shop_name:", store.shop_name)
print("store_type:", store.store_type)
store.describe_shop()
store.open_shop()

print("\n--- b ---")
for s in (Shop("Book Club", "книги"), Shop("Sport Life", "спорттовари"), Shop("Zoo Shop", "зоотовари")):
    s.describe_shop()

print("\n--- c ---")
store = Shop("Rozetka", "електроніка")
print("number_of_units:", store.number_of_units)
store.number_of_units = 120
print("number_of_units після зміни:", store.number_of_units)

print("\n--- d ---")
store.set_number_of_units(250)
print("Після set_number_of_units(250):", store.number_of_units)
store.increment_number_of_units(30)
print("Після increment_number_of_units(30):", store.number_of_units)

print("\n--- e ---")
store_discount = Discount("Rozetka Outlet", "електроніка", ["навушники", "павербанк", "мишка"])
store_discount.describe_shop()
store_discount.get_discounts_ptoducts()
