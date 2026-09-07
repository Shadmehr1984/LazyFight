from moves.Move import Move
from moves.MoveTarget import MoveTarget
from creatures.Creature import Creature

class Heal(Move):
    move_target: MoveTarget = MoveTarget.myself
    
    def __init__(self, rank, value, accurate):
        super().__init__(rank, value, accurate)
    
    def effect(self, owner: Creature):
        if (self.is_take):
            value = self.value * self.rate
            owner.current_hp += value
            if (owner.current_hp > owner.max_hp):
                owner.current_hp = owner.max_hp
    
    def __str__(self) -> str:
        return f'heal, rank:{self.rank}, value:{self.value}, accurate:{self.accurate}'