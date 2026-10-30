from src.creatures.Player import Player
from src.creatures.Group import Group
from src.generators.EnemyGenerator import EnemyGenerator
from src.models.PlayerModel import PlayerModel

class CreateNewPlayerMenu:
    def __init__(self, players: list[Player]) -> None:
        self.players = players
    
    def open(self) -> Player:
        print('----------------------------------------')
        print('CREATE NEW PLAYER MENU')
        print()
        
        print('enter new player\'s name')
        player_input = None
        is_duplicate = False
        name = ''
        while(True):
            player_input = input('name:')
            if (not player_input.isalnum()):
                print('name must be alpha-numeric, try again')
            for player in self.players:
                if player_input == player.name:
                    is_duplicate = True
                    break
            if (is_duplicate):
                print('this name use by another player')
                is_duplicate = False
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
        
        new_player = Player(name, 1, group, 100)
        
        #add 6 basic move
        for move in EnemyGenerator.generate(1, 'rrrrrr', group.name).moves:
            new_player.add_move(move)
        
        #save
        (PlayerModel(new_player)).save()
        
        return new_player