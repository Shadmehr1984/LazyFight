from src.things.Item import Item
from random import randint

class ItemGenerator:
    @staticmethod
    def generate() -> Item:
        available_item_names = [
            'fire-token',
            'iron',
            'earth-token',
            'stone',
            'plant-token',
            'wood',
            'light-token',
            'glass',
            'dark-token',
            'oil'
        ]
        
        index = randint(0, len(available_item_names) - 1)
        
        name = available_item_names[index]
        
        return Item(name, 5)