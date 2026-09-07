from src.fighting.Turn import Turn

class Fight:
    def __init__(self, player, enemy) -> None:
        self.player = player
        self.enemy = enemy
        self.is_win: bool
    
    def start(self):
        self.player.select_fight_moves()
        self.enemy.select_fight_moves()
        print('fight start!')
        fight_continue = True
        turn = Turn(self.player, self.enemy)
        while(fight_continue):
            fight_continue = turn.start()
            print(self.player)
            print(self.enemy)
            print('----------------------------------------')
        print()
        if (self.player.current_hp <= 0 and self.enemy.current_hp <= 0):
            print('both of player and enemy die!')
            self.is_win = False
        elif (self.enemy.current_hp <= 0):
            print('you win!')
            self.player.increase_exp(self.enemy.rank * 10)
            self.is_win = True
        else:
            print('you lose')
            self.is_win = False
        return self.is_win