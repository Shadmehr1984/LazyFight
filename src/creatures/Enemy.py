from creatures.Creature import Creature
from random import randint

class Enemy(Creature):
    def __init__(self, name: str, rank: int, max_hp: int):
        super().__init__(name, rank, max_hp)
    
    def select_fight_moves(self):
        if (len(self.moves) == 6):
            self.fight_moves = self.moves.copy()
        else:
            counter = 0
            while(counter < 6):
                index = randint(0, len(self.moves) - 1)
                if (self.moves[index] not in self.fight_moves):
                    self.fight_moves.append(self.moves[index])
                    counter += 1
        print('enemy select his fight moves')
        print()
    
    def select_turn_moves(self):
        counter = 0
        while(counter < 3):
            index = randint(0, 5)
            if (self.fight_moves[index] not in self.turn_moves):
                self.turn_moves.append(self.fight_moves[index])
                counter += 1
        print('enemy select his turn moves')
        print()