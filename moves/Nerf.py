from moves.Move import Move
from moves.Attack import Attack
from moves.Defend import Defend
from moves.Heal import Heal
from moves.MoveTarget import MoveTarget
from creatures.Creature import Creature

class Nerf(Move):
    move_target: MoveTarget = MoveTarget.opponent
    
    def __init__(self, rank, value, accurate, move_class) -> None:
        if (value < 0):
            raise ValueError("value must be greater or equal 0")
        super().__init__(rank, value, accurate)
        if move_class not in [Attack, Defend, Heal]:
            raise ValueError("move_class must be type of Attack, Defend or Heal")
        self.move_class = move_class
    
    def effect(self, opponent: Creature):
        if (self.is_take):
            opponent.set_moves_rate(-self.value, self.move_class)
    
    def __str__(self) -> str:
        move_class_name = ''
        if (self.move_class == Attack):
            move_class_name = "Attack"
        elif (self.move_class == Defend):
            move_class_name = "Defend"
        elif (self.move_class == Heal):
            move_class_name == "Heal"
        return f'nerf, rank:{self.rank}, value:{self.value}, accurate:{self.accurate}, move class:{move_class_name}'