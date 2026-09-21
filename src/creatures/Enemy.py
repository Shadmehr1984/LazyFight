from src.creatures.Creature import Creature
from src.creatures.Group import Group
from src.creatures.exceptions.NotEnoughMovesException import NotEnoughMoveException
from random import randint

class Enemy(Creature):
    def __init__(self, name: str, rank: int, group: Group, max_hp: int):
        super().__init__(name, rank, group, max_hp)
    
    def select_fight_moves(self):
        if (len(self.moves) < 3):
            raise NotEnoughMoveException()
        
        if (len(self.moves) <= self.fight_moves_size):
            self.fight_moves = self.moves.copy()
        else:
            counter = 0
            while(counter < self.fight_moves_size):
                index = randint(0, len(self.moves) - 1)
                if (self.moves[index] not in self.fight_moves):
                    self.fight_moves.append(self.moves[index])
                    counter += 1
        print('enemy select his fight moves')
        print()
    
    def select_turn_moves(self):
        if (len(self.moves) < 3):
            raise NotEnoughMoveException()
        
        counter = 0
        while(counter < self.turn_moves_size):
            index = randint(0, self.fight_moves_size - 1)
            if (self.fight_moves[index] not in self.turn_moves):
                self.turn_moves.append(self.fight_moves[index])
                counter += 1
        print('enemy select his turn moves')
        print()