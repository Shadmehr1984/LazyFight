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
                print("select player or enter exit to close menu")
                player_input = input('player index:')
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
        while(reopen_menu):
            reopen_menu = (ActivityMenu(self.player)).open()
        
        return True

    def __show_players(self):
        print('players:')
        player_index = 0
        for player in self.players:
            print(f'{player_index}: {player.name} {player.exp} exp')
            player_index += 1