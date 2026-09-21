from src.things.Inventory import Inventory
from src.creatures.Group import Group
from math import fabs

class Creature:
    fight_moves_size = 6
    turn_moves_size = 3
    
    def __init__(self, name: str, rank: int, group: Group, max_hp):
            self.name = name
            self.rank: int = rank
            self.group: Group = group
            self.group_rate = 1
            self.max_hp = max_hp
            self.current_hp: int = max_hp
            self.base_defense = 10
            self.defense: int = 0
            self.inventory: Inventory = Inventory()
            self.moves: list = []
            self.fight_moves: list = []
            self.turn_moves: list = []
            self.effected_moves: list = []
    
    def add_move(self, move):
        self.moves.append(move)
    
    def add_effected_move(self, move):
        self.effected_moves.append(move)
    
    def select_fight_moves(self):
        pass
    
    def clear_fight_moves(self):
        self.fight_moves = []
    
    def select_turn_moves(self):
        pass
    
    def clear_turn_moves(self):
        self.turn_moves = []
    
    def clear_effected_moves(self):
        self.effected_moves = []
    
    def set_base_defense(self, base_defense: int):
        self.base_defense = base_defense
    
    def reset(self):
        self.current_hp = self.max_hp
        self.defense = self.base_defense
        self.fight_moves = []
        self.turn_moves = []
        self.effected_moves = []
    
    def set_moves_rate(self, rate: float, move_class):
        for move in self.moves:
            if type(move) == move_class:
                move.rate = move.rate + rate
    
    def reset_moves_rate(self):
        for move in self.moves:
            move.rate = 1
    
    def set_group_rate(self, opponent_group: Group):
        status = Group.compare(self.group, opponent_group)
        
        match status:
            case 1:
                self.group_rate = 1.25
            case 0:
                self.group_rate = 1
            case -1:
                self.group_rate = 0.75
    
    def reset_group_rate(self):
        self.group_rate = 1
    
    def take_damage(self, damage: int):
        damage = int(damage * fabs(2 - self.group_rate))
        damage_copy = damage
        damage -= self.defense
        self.defense -= damage_copy
        if(self.defense < 0):
            self.defense = 0
        if(damage < 0):
            damage = 0
        self.current_hp -= damage
    
    def get_defend(self, defend: int):
        defend = int(defend * self.group_rate)
        self.defense += defend
    
    def get_heal(self, heal: int):
        heal = int(heal * self.group_rate)
        self.current_hp += heal
        if (self.current_hp > self.max_hp):
            self.current_hp = self.max_hp
    
    def __str__(self) -> str:
        return f'{self.name}, group:{self.group.name}, rank:{self.rank}, hp:{self.current_hp}, defense:{self.defense}'