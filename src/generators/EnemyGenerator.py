from src.creatures.Enemy import Enemy
from src.generators.MoveGenerator import MoveGenerator
from src.generators.InventoryGenerator import InventoryGenerator
from src.creatures.Group import Group
from src.moves.Move import Move
from random import randint

class EnemyGenerator:
    @staticmethod
    def generate(rank: int, name: str, group: str) -> Enemy:
        if (rank < 1):
            raise ValueError(f'invalid rank:{rank}')
        if (group not in ['rock', 'paper', 'scissor']):
            raise ValueError(f'invalid group:{group}')
        
        match group:
            case 'rock':
                group = Group.rock
            case 'paper':
                group = Group.paper
            case 'scissor':
                group = Group.scissor
        
        max_hp = rank * 100
        base_defense = rank * 10
        
        enemy = Enemy(name, rank, group, max_hp)
        enemy.base_defense = base_defense
        
        #add a certain attack
        enemy.add_move(MoveGenerator.generate(rank, 'attack'))
        for i in range(0, 5):
            enemy.add_move(EnemyGenerator.__generate_random_move(rank))
        
        enemy.inventory = InventoryGenerator.generate(rank)
        
        return enemy
    
    @staticmethod
    def __generate_random_move(rank: int) -> Move:
        move_types = ['attack', 'defend', 'heal', 'nerf', 'buff']
        index = randint(0, 4)
        
        move_type = move_types[index]
        
        if (move_type in ['nerf', 'buff']):
            buff_or_nerf_move_classes = ['heal', 'attack', 'defend']
            index = randint(0, 2)
            
            buff_or_nerf_move_class = buff_or_nerf_move_classes[index]
            
            return MoveGenerator.generate(rank, move_type, buff_or_nerf_move_class)
        else:
            return MoveGenerator.generate(rank, move_type)