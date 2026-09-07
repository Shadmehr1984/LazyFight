from src.moves.Defend import Defend
from src.moves.Heal import Heal
from src.moves.Attack import Attack
from src.moves.Buff import Buff
from src.moves.Nerf import Nerf
from src.moves.Move import Move
from src.moves.MoveTarget import MoveTarget
from src.creatures.Player import Player
from src.creatures.Enemy import Enemy
from time import sleep

class Turn:
    move_order: list = [Nerf, Buff, Heal, Defend, Attack]
    turn_moves_count = 3
    
    def __init__(self, player: Player, enemy: Enemy) -> None:
        self.player = player
        self.enemy = enemy
    
    def preparing(self):
        self.player.select_turn_moves()
        self.enemy.select_turn_moves()
    
    def trigger(self):
        for move_index in range(0, self.turn_moves_count):
            self.player.turn_moves[move_index].move_take()
            self.enemy.turn_moves[move_index].move_take()
            self.player.turn_moves[move_index].is_effected(self.player)
            self.enemy.turn_moves[move_index].is_effected(self.enemy)
    
    def execute_moves_effect(self, player_move: Move, enemy_move: Move):
        player_target = None
        enemy_target = None
        
        # 999 means out of order
        player_move_order = 999
        enemy_move_order = 999
        
        if player_move is not None:
            player_target = self.player if player_move.move_target == MoveTarget.myself else self.enemy
            player_move_order = Turn.move_order.index(player_move.__class__)
        if enemy_move is not None:
            enemy_target = self.enemy if enemy_move.move_target == MoveTarget.myself else self.player
            enemy_move_order = Turn.move_order.index(enemy_move.__class__)
        
        execute_order = []
        
        if (player_move_order <= enemy_move_order):
            execute_order.append({'move': player_move, 'target': player_target})
            execute_order.append({'move': enemy_move, 'target': enemy_target})
        else:
            execute_order.append({'move': enemy_move, 'target': enemy_target})
            execute_order.append({'move': player_move, 'target': player_target})
        
        for execute in execute_order:
            if (execute['move'] != None):
                execute['move'].effect(execute['target'])
    
    def reset_creatures(self):
        self.player.clear_turn_moves()
        self.player.clear_effected_moves()
        self.player.reset_moves_rate()
        self.enemy.clear_turn_moves()
        self.enemy.clear_effected_moves()
        self.enemy.reset_moves_rate()
    
    def start(self) -> bool:
        is_continue: bool = True
        self.preparing()
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
        for move_index in range(0, self.turn_moves_count):
            self.execute_moves_effect(self.player.effected_moves[move_index], self.enemy.effected_moves[move_index])
        self.reset_creatures()
        if (self.player.current_hp <= 0 or self.enemy.current_hp <= 0):
            is_continue = False
        return is_continue