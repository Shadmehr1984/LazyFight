from src.fighting.Dungeon import Dungeon
from src.generators.EnemyGenerator import EnemyGenerator
from src.generators.random_name_generator.RandomNameGenerator import RandomNameGenerator
from src.creatures.Player import Player
from random import randint

class DungeonGenerator:
    @staticmethod
    def generate(rank: int, player: Player):
        if (rank < 1):
            raise ValueError(f'invalid rank:{rank}')
        
        enemies = []
        
        if (rank == 1):
            group = DungeonGenerator.__generate_random_group()
            name = RandomNameGenerator.generate()
            enemies.append(EnemyGenerator.generate(rank, name, group))
        else:
            enemies_count = rank
            enemies_rank = 1
            
            for i in range(0, rank):
                for j in range(0, enemies_count):
                    group = DungeonGenerator.__generate_random_group()
                    name = RandomNameGenerator.generate() 
                    enemies.append(EnemyGenerator.generate(enemies_rank, name, group))
                enemies_rank += 1
                enemies_count -= 1
        
        return Dungeon(player, enemies)
    
    @staticmethod
    def __generate_random_group():
        groups = ['rock', 'paper', 'scissor']
        index = randint(0, 2)
        
        group = groups[index]
        
        return group