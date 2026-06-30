from creatures.Creature import Creature

class Player(Creature):
    def __init__(self, name: str, rank: int, max_hp: int):
        self.exp = 0
        super().__init__(name, rank, max_hp)
    
    def rank_up(self):
        self.exp -= self.rank * 100
        self.rank += 1
        self.max_hp = self.rank * 100
        if (self.exp >= self.rank * 100):
            self.rank_up()
    
    def increase_exp(self, exp: int):
        self.exp += exp
        if (self.exp >= self.rank * 100):
            self.rank_up()
    
    def select_fight_moves(self):
        if (len(self.moves) == 6):
            self.fight_moves = self.moves.copy()
        else:
            print('select your fighting moves:')
            for move_index in range(0, len(self.moves)):
                print(move_index, self.moves[move_index])
            print()
            selected_move_index: int
            for counter in range(0, 6):
                print(f'select {counter}th fight move:')
                selected_move_index = int(input())
                self.fight_moves.append(self.moves[selected_move_index])
        print('fight moves selected')
        print()
    
    def select_turn_moves(self):
        print('select your turn moves:')
        for move_index in range(0, 6):
            print(move_index, self.fight_moves[move_index])
        print()
        selected_move_index: int
        for counter in range(0, 3):
            print(f'select {counter}th turn move:')
            selected_move_index = int(input())
            self.turn_moves.append(self.fight_moves[selected_move_index])
        print()
    
    def __str__(self) -> str:
        return f'{self.name}, rank:{self.rank}, hp:{self.current_hp}, defense:{self.defense}, exp:{self.exp}'