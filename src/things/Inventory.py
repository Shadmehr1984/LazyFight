from src.things.Item import Item
from src.things.Exceptions.ItemNotExistException import ItemNotExistException
from src.things.Exceptions.ItemNotEnoughException import ItemNotEnoughException

class Inventory:
    def __init__(self) -> None:
        self.items: dict[str, Item] = {}
    
    def add_item(self, item: Item):
        if (self.exist_item(item.name)):
            self.items[item.name].count += item.count
        else:
            self.items[item.name] = item
    
    def exist_item(self, item_name: str):
        item = self.items.get(item_name)
        return item is not None

    def exist_items(self, items_name: list[str]):
        result = True
        for item_name in items_name:
            result = result and self.exist_item(item_name)
        return result
    
    def enough_item(self, item_name: str, item_count: int):
        if (item_count <= 0):
            raise ValueError("count is a positive value")
        
        item = self.items.get(item_name)
        
        if (item is None):
            raise ItemNotExistException('item not exists')
        
        return item.count >= item_count
    def enough_items(self, items: dict[str, int]):
        result = True
        for item_name in items:
            result = result and self.enough_item(item_name, item_count=items[item_name])
        return result
    
    def pick_item(self, item_name: str, item_count: int):
        if (item_count <= 0):
            raise ValueError("count is a positive value")
        
        item = self.items.get(item_name)
        
        if (item is None):
            raise ItemNotExistException('item not exists')
        
        if (item.count < item_count):
            raise ItemNotEnoughException('not enough item')
        
        item.count -= item_count
        
        if (item.count == 0):
            del self.items[item_name]
        
        return True
    
    def pick_items(self, items: dict[str, int]):
        for item_name in items:
            item_count = items[item_name]
            if (not self.exist_item(item_name)):
                raise ItemNotExistException(f'item {item_name} not exists')
            if (not self.enough_item(item_name, item_count)):
                raise ItemNotEnoughException(f'not enough {item_name}, count:{item_count}')
        
        for item_name in items:
            item_count = items[item_name]
            
            item = self.items[item_name]
            
            item.count -= item_count
            
            if (item.count == 0):
                del self.items[item_name]
        
        return True

    def len(self):
        return len(self.items)
    
    def get(self):
        items : dict[str, int] = {}
        
        for item_name in self.items:
            item_count = self.items[item_name].count
            items[item_name] = item_count
        
        return items
    
    def add_all_inventory(self, inventory: 'Inventory'):
        for item in inventory.items.values():
            self.add_item(item)
    
    def __str__(self) -> str:
        result = ''
        for item in self.items.values():
            result += item.__str__() + "\n"
        return result[0:-1]