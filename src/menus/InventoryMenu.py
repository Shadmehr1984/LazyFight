from src.things.Inventory import Inventory
from src.creatures.Player import Player

class InventoryMenu:
    def __init__(self, player: Player) -> None:
        self.player = player
    
    def open(self):
        print('----------------------------------------')
        print('INVENTORY MENU')
        print()
        print(f'{self.player.name} inventory:')
        print(self.player.inventory)
        
        print()
        input('enter to close menu:')