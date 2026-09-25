from src.menus.PlayersMenu import PlayersMenu
from src.menus.CreateNewPlayerMenu import CreateNewPlayerMenu
from src.creatures.Player import Player

class MainMenu:
    def __init__(self, players: list[Player]) -> None:
        self.players = players
    
    def open(self):
        while(True):
            print('----------------------------------------')
            print('MAIN MENU')
            print()
            
            self.__show_menus()
            
            player_input = None
            menu = None
            while(True):
                print('select a menu or enter exit to close game')
                player_input = input(':')
                if (player_input == 'exit'): return
                if (player_input not in ['0', '1']):
                    print('invalid input, try again')
                else:
                    menu = player_input
                    break
            
            match menu:
                case '0':
                    new_player = (CreateNewPlayerMenu()).open()
                    if (new_player in self.players):
                        print('duplicate player, select another name')
                    else:
                        self.players.append(new_player)
                        print('player created')
                case '1':
                    reopen_menu = True
                    while(reopen_menu):
                        reopen_menu = (PlayersMenu(self.players)).open()
    
    def __show_menus(self):
        print('0 create new player')
        print('1 select a player')
        print()