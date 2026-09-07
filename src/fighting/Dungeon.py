from src.fighting.Fight import Fight
from src.things.Inventory import Inventory

class Dungeon:
    def __init__(self, player, enemies) -> None:
        self.player = player
        self.enemies = enemies
        self.inventory: Inventory = Inventory()
        self.make_dungeon_inventory()
    
    def make_dungeon_inventory(self):
        for enemy in self.enemies:
            self.inventory.add_all_inventory(enemy.inventory)
    
    def start(self):
        print('dungeon was open!')
        print('dungeon enemies:')
        for enemy in self.enemies:
            print(enemy)
        print()
        is_win : bool
        for enemy in self.enemies:
            print(f'your opponent:', enemy)
            print()
            is_win = Fight(self.player, enemy).start()
            if (not is_win):
                print('dungeon take you in dark...')
                print()
                return False
        print('now dungeon is clear!')
        print('enemies items:')
        print(self.inventory)
        self.player.inventory.add_all_inventory(self.inventory)
        print()
        self.player.reset()
        return True