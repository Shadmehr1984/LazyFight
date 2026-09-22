from src.generators.ItemGenerator import ItemGenerator
from src.things.Inventory import Inventory
from src.things.Item import Item

class InventoryGenerator:
    @staticmethod
    def generate(rank: int):
        if (rank < 1):
            raise ValueError(f'invalid rank:{rank}')
        
        inventory = Inventory()
        
        for i in range(0, rank * 2):
            item = ItemGenerator.generate()
            inventory.add_item(item)
        
        #add a basic coin
        coin_count = 10 + (rank * 5)
        inventory.add_item(Item('coin', coin_count))
        
        return inventory