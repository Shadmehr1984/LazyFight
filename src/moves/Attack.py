from src.moves.Move import Move
from src.moves.MoveTarget import MoveTarget
from src.creatures.Creature import Creature

class Attack(Move):
    move_target: MoveTarget = MoveTarget.opponent
    
    def __init__(self, rank, value, accurate):
        super().__init__(rank, value, accurate)
    
    def effect(self, opponent: Creature):
        if (self.is_take):
            value = int(self.value * self.rate)
            opponent.take_damage(value)
    
    def __str__(self) -> str:
        return f'attack, rank:{self.rank}, value:{self.value}, accurate:{self.accurate}'