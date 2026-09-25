from src.chests.ItemChest import ItemChest
from src.chests.MoveChest import MoveChest
from src.chests.Chest import Chest
from src.moves.Move import Move
from src.things.Item import Item
from random import randint
from src.generators.MoveGenerator import MoveGenerator
from src.generators.ItemGenerator import ItemGenerator

class ChestGenerator:
    @staticmethod
    def generate(rank: int, chest_content: str) -> Chest:
        if (rank < 1):
            raise ValueError(f'invalid rank:{rank}')
        if (chest_content not in ['move', 'item']):
            raise ValueError('chest content must be move or item')
        
        match chest_content:
            case 'move':
                moves = []
                for i in range(0, 3):
                    moves.append(ChestGenerator.__generate_random_move(rank))
                
                chest = MoveChest(rank, moves)
                return chest
            case 'item':
                items = []
                for i in range(0, 3):
                    items.append(ChestGenerator.__generate_random_item(rank))
                
                chest = ItemChest(rank, items)
                return chest
    
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
    
    @staticmethod
    def __generate_random_item(rank: int) -> Item:
        item = ItemGenerator.generate()
        if (rank > 1):
            item.count *= rank
        
        return item 