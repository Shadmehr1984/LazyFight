from src.moves.Move import Move
from src.creatures.Player import Player

class MovesMenu:
    def __init__(self, player: Player) -> None:
        self.player = player
    
    #if return True means menu should open again 
    def open(self) -> bool:
        print('----------------------------------------')
        print('MOVES MENU')
        print()
        self.__show_moves()
        print()
        print('select a move for rank up or print exit to close menu')
        
        player_input = None
        move_index = None
        while(True):
            try:
                player_input = input('move index:')
                if (player_input == 'exit'): return False
                move_index = int(player_input)
                if (move_index not in range(0, len(self.player.moves))):
                    raise ValueError()
                break
            except ValueError:
                print('invalid input, try again')
        
        move: Move = self.player.moves[move_index]
        print('rank up require items:')
        for item_name in move.rank_up_require:
            item_count = move.rank_up_require[item_name]
            print(f'name:{item_name}, count:{item_count}')
        
        player_inventory = self.player.inventory
        for item_name in move.rank_up_require:
            item_count = move.rank_up_require[item_name]
            if (not player_inventory.exist_item(item_name)):
                print(f'you don\'t have this item:{item_name}')
                return True
            if (not player_inventory.enough_item(item_name, item_count)):
                print(f'you have not enough of this item:{item_name}')
                print(f'your count:{player_inventory.get()[item_name]}')
                return True
        
        commit = None
        while(True):
            try:
                player_input = input('rank up move?(y/n):')
                if (player_input in ['Y', 'y', 'N', 'n']):
                    match player_input:
                        case 'Y':
                            commit = True
                        case 'y':
                            commit = True
                        case 'N':
                            commit = False
                        case 'n':
                            commit = True
                    break
                else: raise ValueError()
            except ValueError:
                print('invalid input, try again')
        
        if (commit):
            move.rank_up(player_inventory)
            print(move)
        
        return True

    def __show_moves(self):
        move_index = 0
        
        for move in self.player.moves:
            print(f'{move_index}: {move}')
            move_index += 1