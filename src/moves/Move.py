from src.creatures.Creature import Creature
from src.moves.MoveTarget import MoveTarget
from random import randint

class Move:
    move_target: MoveTarget = None
    
    def __init__(self, rank, value, accurate) -> None:
        self.rank = rank
        self.value = value
        self.accurate = accurate
        self.is_take: bool
        self.rate: float = 1
    
    def move_take(self):
        self.is_take = randint(0, 100) <= self.accurate
    
    def is_effected(self, move_owner):
        if (self.is_take):
            move_owner.add_effected_move(self)
        else: move_owner.add_effected_move(None)
    
    def effect(self, creature: Creature):
        pass