from src.menus.SinglePlayerMenu import SinglePlayerMenu
from src.fighting.Dungeon import Dungeon
from src.generators.DungeonGenerator import DungeonGenerator
from src.creatures.Player import Player

class DungeonsMenu(SinglePlayerMenu):
    def __init__(self, player: Player) -> None:
        self.player = player
    
    #if return True means menu should open again 
    def open(self) -> True:
        print('----------------------------------------')
        print("DUNGEONS MENU")
        print()
        print(f'select dungeon rank from 1 up to {self.player.rank}')
        print('enter exit for close menu')
        player_input = input('dungeon rank:')
        
        if (player_input == 'exit'): return False
        
        dungeon_rank = None
        
        while(True):
            try:
                dungeon_rank = int(player_input)
                if (dungeon_rank not in range(1, self.player.rank + 1)):
                    print('invalid dungeon rank try again')
                    dungeon_rank = int(input('dungeon rank:'))
                else: break
            except(ValueError):
                print('invalid input, try again')
                player_input = input('dungeon rank:')
                if (player_input == 'exit'): return False
        
        dungeon = self.__generate_dungeon(dungeon_rank)
        
        dungeon.start()
        
        return True
    
    def __generate_dungeon(self, dungeon_rank: int) -> Dungeon:
        return DungeonGenerator.generate(dungeon_rank, self.player)