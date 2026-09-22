from src.moves.Move import Move
from src.moves.MoveTarget import MoveTarget
from src.creatures.Creature import Creature

class Heal(Move):
    move_target: MoveTarget = MoveTarget.myself
    
    __BASE_VALUE = 20
    __BASE_ACCURATE = 30
    __BASE_RANK_UP_REQUIRE = {'plant-token':5, 'wood': 15}
    
    def __init__(self, rank, value, accurate, rank_up_require: dict[str, int]):
        super().__init__(rank, value, accurate, rank_up_require)
    
    def effect(self, owner: Creature):
        if (self.is_take):
            value = int(self.value * self.rate)
            owner.get_heal(value)
    
    def __str__(self) -> str:
        return f'heal, rank:{self.rank}, value:{self.value}, accurate:{self.accurate}'