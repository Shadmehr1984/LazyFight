from creatures.Creature import Creature
from random import randint

class Move:
    def __init__(self, rank, value, accurate) -> None:
        self.rank = rank
        self.value = value
        self.accurate = accurate
        self.is_take: bool
    
    def move_take(self):
        self.is_take = randint(0, 100) <= self.accurate
    
    def is_effected(self, move_owner):
        if (self.is_take):
            move_owner.effected_moves.append(self)
        else: move_owner.effected_moves.append(None)
    
    def effect(self, creature: Creature):
        pass