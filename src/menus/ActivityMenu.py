from src.menus.SinglePlayerMenu import SinglePlayerMenu
from src.creatures.Player import Player
from src.menus.DungeonsMenu import DungeonsMenu
from src.menus.InventoryMenu import InventoryMenu
from src.menus.MovesMenu import MovesMenu

class ActivityMenu(SinglePlayerMenu):
    menus = [DungeonsMenu, MovesMenu, InventoryMenu]
    
    def __init__(self, player: Player) -> None:
        self.player = player
    
    def open(self) -> bool:
        print('----------------------------------------')
        print('ACTIVITY MENU')
        print()
        
        self.__show_menus()
        
        player_input = None
        menu = None
        while(True):
            try:
                print('select menu or enter exit to close menu')
                player_input = input('menu index:')
                if (player_input == "exit"): return False
                
                menu_index = int(player_input)
                if (menu_index not in range(0, len(ActivityMenu.menus))):
                    print('invalid menu index, try again')
                else:
                    menu = ActivityMenu.menus[menu_index]
                    break
            except ValueError:
                print('invalid input, try again')
        
        reopen_menu = True
        while(reopen_menu):
            reopen_menu = (menu(self.player)).open()
        
        return True

    def __show_menus(self):
        print('menus:')
        print('0 dungeon menu')
        print('1 moves menu')
        print('2 inventory menu')