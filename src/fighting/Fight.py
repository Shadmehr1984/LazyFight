from src.fighting.Turn import Turn
from src.creatures.Player import Player
from src.creatures.Enemy import Enemy

class Fight:
    rank_2_exp_rate = 10
    
    def __init__(self, player: Player, enemy: Enemy) -> None:
        self.player: Player = player
        self.enemy: Enemy = enemy
        self.is_win: bool
    
    def preparing(self):
        self.player.select_fight_moves()
        self.enemy.select_fight_moves()
        self.player.set_group_rate(self.enemy.group)
        self.enemy.set_group_rate(self.player.group)
    
    def fight(self):
        fight_continue = True
        turn = Turn(self.player, self.enemy)
        while(fight_continue):
            fight_continue = turn.start()
            print(self.player)
            print(self.enemy)
            print('----------------------------------------')
    
    def reset_creatures(self):
        self.player.reset_group_rate()
        self.enemy.reset_group_rate()
    
    def set_fight_result(self):
        if (self.player.current_hp <= 0 and self.enemy.current_hp <= 0):
            print('both of player and enemy die!')
            self.is_win = False
        elif (self.enemy.current_hp <= 0):
            print('you win!')
            self.player.increase_exp(self.enemy.rank * self.rank_2_exp_rate)
            self.is_win = True
        else:
            print('you lose')
            self.is_win = False
    
    def start(self):
        self.preparing()
        print('fight start!')
        self.fight()
        self.reset_creatures()
        print()
        self.set_fight_result()
        return self.is_win