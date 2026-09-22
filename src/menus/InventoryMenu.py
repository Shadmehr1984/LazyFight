from src.menus.SinglePlayerMenu import SinglePlayerMenu
from src.creatures.Player import Player

class InventoryMenu(SinglePlayerMenu):
    def __init__(self, player: Player) -> None:
        self.player = player
    
    def open(self) -> bool:
        print('----------------------------------------')
        print('INVENTORY MENU')
        print()
        print(f'{self.player.name} inventory:')
        if (self.player.inventory.len() == 0):
            print('inventory is empty...')
        else:
            print(self.player.inventory)
        
        print()
        input('enter to close menu:')