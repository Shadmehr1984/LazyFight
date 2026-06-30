from moves.Move import Move
from creatures.Creature import Creature

class Attack(Move):
    def __init__(self, rank, value, accurate):
        super().__init__(rank, value, accurate)
    
    def effect(self, opponent: Creature):
        if (self.is_take):
            value = self.value
            value -= opponent.defense
            opponent.defense -= self.value
            if(opponent.defense < 0):
                opponent.defense = 0
            if(value < 0):
                value = 0
            opponent.current_hp -= value
    
    def __str__(self) -> str:
        return f'attack, rank:{self.rank}, value:{self.value}, accurate:{self.accurate}'