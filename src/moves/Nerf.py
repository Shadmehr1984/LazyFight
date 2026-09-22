from src.moves.Move import Move
from src.moves.Attack import Attack
from src.moves.Defend import Defend
from src.moves.Heal import Heal
from src.moves.MoveTarget import MoveTarget
from src.creatures.Creature import Creature
from src.things.Inventory import Inventory
from math import ceil

class Nerf(Move):
    move_target: MoveTarget = MoveTarget.opponent
    
    __BUFF_AND_NERF_VALUE_RANK_UP_RATE = 0.1
    
    __BASE_VALUE = 0.5
    __BASE_ACCURATE = 70
    __BASE_RANK_UP_REQUIRE =  {'dark-token':15, 'oil': 20}
    
    def __init__(self, rank, value, accurate, move_class, rank_up_require: dict[str, int]) -> None:
        if (value < 0):
            raise ValueError("value must be greater or equal 0")
        super().__init__(rank, value, accurate, rank_up_require)
        if move_class not in [Attack, Defend, Heal]:
            raise ValueError("move_class must be type of Attack, Defend or Heal")
        self.move_class = move_class
    
    def rank_up(self, inventory: Inventory):
        try:
            inventory.pick_items(self.rank_up_require)
        except IndexError as e:
            return False
        except ValueError as e:
            return False
        
        self.rank += 1
        self.value = self.value + Nerf._Nerf__BUFF_AND_NERF_VALUE_RANK_UP_RATE
        if (self.accurate < 100): self.accurate = ceil(self.accurate + (self.accurate/Move._Move__ACCURATE_RANK_UP_RATE))
        if (self.accurate > 100): self.accurate = 100
        for item_name in self.rank_up_require:
            self.rank_up_require[item_name] = ceil(self.rank_up_require[item_name] + (self.rank_up_require[item_name]/Move._Move__RANK_UP_REQUIRE_ITEM_COUNT_RATE))
    
    def effect(self, opponent: Creature):
        if (self.is_take):
            value = -self.value
            opponent.set_moves_rate(value, self.move_class)
    
    def __str__(self) -> str:
        move_class_name = ''
        if (self.move_class == Attack):
            move_class_name = "Attack"
        elif (self.move_class == Defend):
            move_class_name = "Defend"
        elif (self.move_class == Heal):
            move_class_name = "Heal"
        
        return f'nerf, rank:{self.rank}, value:{self.value}, accurate:{self.accurate}, move class:{move_class_name}'