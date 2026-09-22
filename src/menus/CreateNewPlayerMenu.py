from src.creatures.Player import Player
from src.creatures.Group import Group

class CreateNewPlayerMenu:
    def __init__(self) -> None:
        pass
    
    def open(self) -> Player:
        print('----------------------------------------')
        print('CREATE NEW PLAYER MENU')
        print()
        
        print('enter new player\'s name')
        player_input = None
        name = ''
        while(True):
            player_input = input('name:')
            if (not player_input.isalnum()):
                print('name must be alpha-numeric, try again')
            else:
                name = player_input
                break
        
        print('select a group(rock, paper, scissor)')
        group = ''
        while(True):
            player_input = input('group:')
            if (player_input not in ['rock', 'paper', 'scissor']):
                print('invalid group, try again')
            else:
                group = player_input
                break
        
        match group:
            case 'rock':
                group = Group.rock
            case 'paper':
                group = Group.paper
            case 'scissor':
                group = Group.scissor
        
        return Player(name, 1, group, 100)