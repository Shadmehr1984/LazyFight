class Item:
    def __init__(self, name, count) -> None:
        if (count <= 0):
            raise ValueError("count is a positive value")
        self.name = name
        self.count = count
    
    def get(self):
        return {'name': self.name, 'count': self.count}
    
    def __eq__(self, __value: 'Item') -> bool:
        return self.name == __value.name
    
    def __str__(self) -> str:
        return f'name:{self.name}, count:{self.count}'