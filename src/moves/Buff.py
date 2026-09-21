from src.moves.Move import Move
from src.moves.MoveTarget import MoveTarget
from src.moves.Attack import Attack
from src.moves.Defend import Defend
from src.moves.Heal import Heal
from src.creatures.Creature import Creature

class Buff(Move):
    move_target: MoveTarget = MoveTarget.myself
    
    def __init__(self, rank, value, accurate, move_class, rank_up_require: dict[str, int]) -> None:
        if (value < 0):
            raise ValueError("value must be greater or equal 0")
        super().__init__(rank, value, accurate, rank_up_require)
        if move_class not in [Attack, Defend, Heal]:
            raise ValueError("move_class must be type of Attack, Defend or Heal")
        self.move_class = move_class
    
    def effect(self, owner: Creature):
        if (self.is_take):
            value = self.value
            owner.set_moves_rate(value, self.move_class)
    
    def __str__(self) -> str:
        move_class_name = ''
        if (self.move_class == Attack):
            move_class_name = "Attack"
        elif (self.move_class == Defend):
            move_class_name = "Defend"
        elif (self.move_class == Heal):
            move_class_name = "Heal"
        
        return f'buff, rank:{self.rank}, value:{self.value}, accurate:{self.accurate}, move class:{move_class_name}'