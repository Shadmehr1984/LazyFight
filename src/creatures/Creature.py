from things.Inventory import Inventory

class Creature:
    
    def __init__(self, name: str, rank: int, max_hp):
            self.name = name
            self.rank: int = rank
            self.max_hp = max_hp
            self.current_hp: int = max_hp
            self.base_defense = 0
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
    
    def take_damage(self, damage: int):
        damage -= self.defense
        self.defense -= self.damage
        if(self.defense < 0):
            self.defense = 0
        if(damage < 0):
            damage = 0
        self.current_hp -= damage
    
    def get_defend(self, defend: int):
        self.defense += defend
    
    def get_heal(self, heal: int):
        self.current_hp += heal
        if (self.current_hp > self.max_hp):
            self.current_hp = self.max_hp
    
    def __str__(self) -> str:
        return f'{self.name}, rank:{self.rank}, hp:{self.current_hp}, defense:{self.defense}'