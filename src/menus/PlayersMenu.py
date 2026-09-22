from src.creatures.Player import Player
from src.menus.ActivityMenu import ActivityMenu

class PlayersMenu:
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.player: Player = None
    
    #if return True means menu should open again 
    def open(self) -> bool:
        print('----------------------------------------')
        print('PLAYERS MENU')
        print()
        
        self.__show_players()
        
        player_input = None
        while(True):
            try:
                player_input = input('select player or enter exit to close the game')
                if (player_input == 'exit'): return False
                
                player_index = int(player_input)
                if (player_index not in range(0, len(self.players))):
                    print('invalid player index, try again')
                else:
                    self.player = self.players[player_index]
                    break
            except ValueError:
                print('invalid input, try again')
        
        reopen_menu = True
        while(True):
            reopen_menu = (ActivityMenu(self.player)).open()

    def __show_players(self):
        print('players:')
        for player in self.players:
            print(f'{player.name} {player.exp} exp')