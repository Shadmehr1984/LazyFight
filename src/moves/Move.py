from src.creatures.Creature import Creature
from src.moves.MoveTarget import MoveTarget
from src.things.Inventory import Inventory
from random import randint
from math import ceil

class Move:
    move_target: MoveTarget = None
    
    __VALUE_RANK_UP_RATE = 20
    __ACCURATE_RANK_UP_RATE = 35
    __RANK_UP_REQUIRE_ITEM_COUNT_RATE = 2
    
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
        self.value = ceil(self.value + (self.value/Move._Move__VALUE_RANK_UP_RATE))
        if (self.accurate < 100): self.accurate = ceil(self.accurate + (self.accurate/Move._Move__ACCURATE_RANK_UP_RATE))
        if (self.accurate > 100): self.accurate = 100
        for item_name in self.rank_up_require:
            self.rank_up_require[item_name] = ceil(self.rank_up_require[item_name] + (self.rank_up_require[item_name]/Move._Move__RANK_UP_REQUIRE_ITEM_COUNT_RATE))
    
    def move_take(self):
        self.is_take = randint(0, 100) <= self.accurate
    
    def is_effected(self, move_owner):
        if (self.is_take):
            move_owner.add_effected_move(self)
        else: move_owner.add_effected_move(None)
    
    def effect(self, creature: Creature):
        pass