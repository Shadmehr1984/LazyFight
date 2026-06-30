from moves.Defend import Defend
from moves.Heal import Heal
from time import sleep

class Turn:
    def __init__(self, player, enemy) -> None:
        self.player = player
        self.enemy = enemy
    
    def trigger(self):
        for move_index in range(0, 3):
            self.player.turn_moves[move_index].move_take()
            self.enemy.turn_moves[move_index].move_take()
            self.player.turn_moves[move_index].is_effected(self.player)
            self.enemy.turn_moves[move_index].is_effected(self.enemy)
    
    def start(self) -> bool:
        is_continue: bool = True
        self.player.select_turn_moves()
        self.enemy.select_turn_moves()
        print('player turn moves:')
        for move in self.player.turn_moves:
            print(move)
        print()
        print('enemy turn moves:')
        for move in self.enemy.turn_moves:
            print(move)
        print()
        print('lets trigger it!!!')
        sleep(3)
        print()
        self.trigger()
        player_move_take = False
        enemy_move_take = False
        for move_index in range(0, 3):
            if (type(self.player.effected_moves[move_index]) in [Heal, Defend]):
                self.player.effected_moves[move_index].effect(self.player)
                player_move_take = True
            if (type(self.enemy.effected_moves[move_index]) in [Heal, Defend]):
                self.enemy.effected_moves[move_index].effect(self.enemy)
                enemy_move_take = True
            if (not player_move_take and self.player.effected_moves[move_index] != None):
                self.player.effected_moves[move_index].effect(self.enemy)
            if (not enemy_move_take and self.enemy.effected_moves[move_index] != None):
                self.enemy.effected_moves[move_index].effect(self.player)
            player_move_take = False
            enemy_move_take = False
        self.player.clear_turn_moves()
        self.player.clear_effected_moves()
        self.enemy.clear_turn_moves()
        self.enemy.clear_effected_moves()
        if (self.player.current_hp <= 0 or self.enemy.current_hp <= 0):
            is_continue = False
        return is_continue