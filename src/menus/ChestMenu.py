from src.creatures.Player import Player
from src.menus.SinglePlayerMenu import SinglePlayerMenu
from src.generators.ChestGenerator import ChestGenerator
from src.chests.Chest import Chest
from src.chests.exceptions.NotEnoughCoinException import NotEnoughCoinException
from src.moves.Move import Move
from src.things.Item import Item

class ChestMenu(SinglePlayerMenu):
    def __init__(self, player: Player) -> None:
        super().__init__(player)
    
    def open(self) -> bool:
        print('----------------------------------------')
        print("CHEST MENU")
        print()
        
        chests = self.__generate_chests()
        
        self.__show_chests(chests)
        
        player_input = None
        while(True):
            try:
                print('select chest or enter exit to close menu')
                player_input = input('chest index: ')
                if (player_input == 'exit'): return False
                chest_index = int(player_input)
                if (chest_index not in range(0, len(chests))):
                    print('invalid chest index, try again')
                else:
                    chest = chests[chest_index]
                    chest_content = chest.open(self.player.inventory)
                    print('!!!')
                    print(f'chest content: {chest_content}')
                    print('!!!')
                    #fill chests again
                    chests = self.__generate_chests()
                    if (isinstance(chest_content, Move)):
                        self.player.add_move(chest_content)
                    elif (isinstance(chest_content, Item)):
                        self.player.inventory.add_item(chest_content)
            except NotEnoughCoinException:
                coins = self.player.inventory.items.get('coin')
                coins_count = 0
                if (coins):
                    coins_count = coins.count
                print(f'not enough coin, your coins:{coins_count}')
            except Exception:
                print('invalid input, try again')
        
        return True
    
    def __generate_chests(self) -> list[Chest]:
        chests = []
        
        chests.append(ChestGenerator.generate(1, 'move'))
        chests.append(ChestGenerator.generate(1, 'item'))
        
        if (self.player.rank > 1):
            for chest_rank in range(2, self.player.rank + 1):
                chests.append(ChestGenerator.generate(chest_rank, 'move'))
                chests.append(ChestGenerator.generate(chest_rank, 'item'))
        
        return chests
    
    def __show_chests(self, chests: list[Chest]):
        chest_index = 0
        for chest in chests:
            print(f'{chest_index} {chest}')
            chest_index += 1