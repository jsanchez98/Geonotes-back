from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class InventoryItem:
    _name: str
    _unit_price: Decimal
    _quantity_on_hand: int

    def total_cost(self) -> float:
        return (self.unit_price * self.quantity_on_hand) / 10

    @property
    def name(self):
        return self._name

    @property
    def unit_price(self):
        return self._unit_price

    @unit_price.setter
    def unit_price(self, new_price):
        if new_price > 0 and isinstance(new_price, Decimal):
            self._unit_price = new_price
        else:
            raise ValueError

    @unit_price.getter
    def unit_price(self):
        return self._unit_price


if __name__ == '__main__':
    print("running")
    while True:
        try:
            name = str(input("Please enter the product's name: "))
            price = input("Please enter the price: ")
            quantity = int(input("Please enter a quantity: "))
            inventory_item0 = InventoryItem(name, Decimal(price), quantity)
            break
        except ValueError:
            print("Oops! That wasn't an int. Please try again")

    print(inventory_item0.name)
    print("price: " + str(inventory_item0.unit_price))
    print(type(inventory_item0))
    print(type(InventoryItem))
    inventory_item = InventoryItem("first", 7000, 3)
