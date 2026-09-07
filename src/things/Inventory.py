class Inventory:
    def __init__(self) -> None:
        self.items = []
    
    def add_item(self, item):
        for item_index in range(0, len(self.items)):
            if (item == self.items[item_index]):
                self.items[item_index].count += item.count
                return
        self.items.append(item)
    
    def pick_item(self, item_name, item_count):
        for item_index in range(0, len(self.items)):
            if (item_name == self.items[item_index].name):
                if (item_count > self.items[item_index].count):
                    raise ValueError(f'not enough {item_name}, existing count:{self.items[item_index].count}')
                else:
                    self.items[item_index].count -= item_count
                    if (self.items[item_index].count == 0):
                        self.items.pop(item_index)
                return True
        print('you don\'t have this item')
        return False
    
    def add_all_inventory(self, inventory):
        for item in inventory.items:
            self.add_item(item)
    
    def __str__(self) -> str:
        result = ''
        for item in self.items:
            result += item.__str__() + "\n"
        return result[0:-1]