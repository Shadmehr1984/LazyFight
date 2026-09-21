from src.creatures.Creature import Creature
from src.moves.MoveTarget import MoveTarget
from src.things.Inventory import Inventory
from random import randint

class Move:
    move_target: MoveTarget = None
    
    __VALUE_RANK_UP_RATE = 20
    __ACCURATE_RANK_UP_RATE = 50
    
    def __init__(self, rank, value, accurate, rank_up_require: dict[str, int]) -> None:
        self.rank = rank
        self.value = value
        self.accurate = accurate
        self.rank_up_require = rank_up_require
        self.is_take: bool
        self.rate: float = 1
    
    def rank_up(self, inventory: Inventory):
        try:
            inventory.pick_items(self.rank_up_require)
        except IndexError as e:
            return False
        except ValueError as e:
            return False
        
        self.rank += 1
        self.value = int(self.value + (self.value/Move.__VALUE_RANK_UP_RATE))
        self.accurate = int(self.accurate + (self.accurate/Move.__ACCURATE_RANK_UP_RATE))
    
    def move_take(self):
        self.is_take = randint(0, 100) <= self.accurate
    
    def is_effected(self, move_owner):
        if (self.is_take):
            move_owner.add_effected_move(self)
        else: move_owner.add_effected_move(None)
    
    def effect(self, creature: Creature):
        pass