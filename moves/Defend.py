from moves.Move import Move
from moves.MoveTarget import MoveTarget
from creatures.Creature import Creature

class Defend(Move):
    move_target: MoveTarget = MoveTarget.myself
    
    def __init__(self, rank, value, accurate):
        super().__init__(rank, value, accurate)
    
    def effect(self, owner: Creature):
        if (self.is_take):
            value = self.value * self.rate
            owner.defense += value
    
    def __str__(self) -> str:
        return f'defend, rank:{self.rank}, value{self.value}, accurate:{self.accurate}'