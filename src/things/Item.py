class Item:
    def __init__(self, name, count) -> None:
        self.name = name
        self.count = count
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    
    def __str__(self) -> str:
        return f'name:{self.name}, count:{self.count}'