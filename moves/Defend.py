from moves.Move import Move
from creatures.Creature import Creature

class Defend(Move):
    def __init__(self, rank, value, accurate):
        super().__init__(rank, value, accurate)
    
    def effect(self, owner: Creature):
        if (self.is_take):
            owner.defense += self.value
    
    def __str__(self) -> str:
        return f'defend, rank:{self.rank}, value{self.value}, accurate:{self.accurate}'