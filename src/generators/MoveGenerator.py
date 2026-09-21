from src.moves.Move import Move
from src.moves.Attack import Attack
from src.moves.Buff import Buff
from src.moves.Defend import Defend
from src.moves.Heal import Heal
from src.moves.Nerf import Nerf
from math import ceil

class MoveGenerator:
    @staticmethod
    def generate(rank: int, move_type: str, buff_or_nerf_move_class = None) -> Move:
        if (rank < 1):
            raise ValueError(f'invalid rank{rank}')
        if (move_type not in ['attack', 'defend', 'heal', 'buff', 'nerf']):
            raise ValueError(f'invalid move type:{move_type}')
        has_buff_or_nerf_move_class = False
        if (move_type in ['buff', 'nerf']):
            if (buff_or_nerf_move_class not in ['attack', 'heal', 'defend']):
                raise ValueError(f'invalid move target:{buff_or_nerf_move_class}')
            else: has_buff_or_nerf_move_class = True
        
        base_value = None
        base_accurate = None
        base_rank_up_require = None
        
        move_class = None
        
        match move_type:
            case 'attack':
                base_value = Attack._Attack__BASE_VALUE
                base_accurate = Attack._Attack__BASE_ACCURATE
                base_rank_up_require = {'fire-token': 5, 'iron': 5}
                move_class = Attack
            case 'defend':
                base_value = Defend._Defend__BASE_VALUE
                base_accurate = Defend._Defend__BASE_ACCURATE
                base_rank_up_require = {'earth-token': 5, 'stone': 5}
                move_class = Defend
            case 'heal':
                base_value = Heal._Heal__BASE_VALUE
                base_accurate = Heal._Heal__BASE_ACCURATE
                base_rank_up_require = {'plant-token':5, 'wood': 15}
                move_class = Heal
            case 'buff':
                base_value = Buff._Buff__BASE_VALUE
                base_accurate = Buff._Buff__BASE_ACCURATE
                base_rank_up_require = {'light-token':15, 'glass': 20}
                move_class = Buff
            case 'nerf':
                base_value = Nerf._Nerf__BASE_VALUE
                base_accurate = Nerf._Nerf__BASE_ACCURATE
                base_rank_up_require = {'dark-token':15, 'oil': 20}
                move_class = Nerf
        
        match buff_or_nerf_move_class:
            case 'attack':
                buff_or_nerf_move_class = Attack
            case 'heal':
                buff_or_nerf_move_class = Heal
            case 'defend':
                buff_or_nerf_move_class = Defend
        
        value = MoveGenerator.__calculate_value(rank, base_value, has_buff_or_nerf_move_class)
        accurate = MoveGenerator.__calculate_accurate(rank, base_accurate)
        rank_up_require = MoveGenerator.__calculate_rank_up_require(rank, base_rank_up_require)
        
        if (has_buff_or_nerf_move_class):
            return move_class(rank, value, accurate, buff_or_nerf_move_class, rank_up_require)
        else :
            return move_class(rank, value, accurate, rank_up_require)
    
    @staticmethod
    def __calculate_value(rank: int, base: int, is_buff_or_nerf = False):
        if (rank == 1): return base
        
        if (is_buff_or_nerf):
            #buff and nerf special rate are equal
            rate = Nerf._Nerf__BUFF_AND_NERF_VALUE_RANK_UP_RATE
        
            for i in range(2, rank + 1):
                base = base + rate
        
        else:
            rate = Move._Move__VALUE_RANK_UP_RATE
        
            for i in range(2, rank + 1):
                base = ceil(base + (base/rate))
        
        return base
    
    @staticmethod
    def __calculate_accurate(rank: int, base: int):
        if (rank == 1): return base
        
        rate = Move._Move__ACCURATE_RANK_UP_RATE
        
        for i in range(2, rank + 1):
            base = ceil(base + (base/rate))
            if base > 100 : base = 100
        return base
    
    @staticmethod
    def __calculate_rank_up_require(rank, base: dict):
        if (rank == 1): return base
        
        rate = Move._Move__RANK_UP_REQUIRE_ITEM_COUNT_RATE
        
        for i in range(2, rank + 1):
            for item_name in base:
                base[item_name] = ceil(base[item_name] + (base[item_name]/rate))