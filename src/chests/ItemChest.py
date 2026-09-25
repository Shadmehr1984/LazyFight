from src.things.Item import Item
from src.chests.exceptions.NotEnoughItemsForChestException import NotEnoughItemsForChestException
from src.chests.exceptions.NotValidItemCountException import NotValidItemCountException
from src.chests.exceptions.NotEnoughCoinException import NotEnoughCoinException
from src.things.Inventory import Inventory
from random import randint

class ItemChest:
    def __init__(self, rank: int, items: list[Item]) -> None:
        if (rank < 1):
            raise ValueError(f"invalid rank{rank}")
        if (len(items) < 3):
            raise NotEnoughItemsForChestException("at least 3 item")
        for item in items:
            if (item.count != rank * 5):
                raise NotValidItemCountException()
        self.rank = rank
        self.items = items
        self.price = 50 + (rank * 20)
    
    def open(self, inventory: Inventory) -> Item:
        try:
            if (inventory.pick_item('coin', self.price)):
                index = randint(0, len(self.items) - 1)
                item = self.items[index]
                return item
        except Exception:
            coins = inventory.items.get('coin')
            coins_count = None
            if (coins is None):
                coins_count = 0
            else:
                coins_count = coins.count
            raise NotEnoughCoinException(f'not enough coins, your coins:{coins_count}')
    
    def __str__(self) -> str:
        return f"item chest, rank:{self.rank}, price:{self.price}"