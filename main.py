from creatures.Player import Player
from creatures.Enemy import Enemy
from moves.Attack import Attack
from moves.Defend import Defend
from moves.Heal import Heal
from fighting.Dungeon import Dungeon
from things.Item import Item

player = Player("shady", 1, 100)
enemy1 = Enemy('khamen', 1, 100)
player.add_move(Attack(1, 90, 100))
player.add_move(Attack(1, 10, 100))
player.add_move(Attack(1, 20, 50))
player.add_move(Defend(1, 10, 90))
player.add_move(Defend(1, 10, 90))
player.add_move(Heal(1, 30, 40))

enemy1.add_move(Attack(1, 10, 100))
enemy1.add_move(Attack(1, 10, 100))
enemy1.add_move(Attack(1, 20, 50))
enemy1.add_move(Defend(1, 10, 90))
enemy1.add_move(Defend(1, 10, 90))
enemy1.add_move(Heal(1, 30, 40))
enemy1.inventory.add_item(Item('kir-khar', 5))

enemy2 = Enemy('moshtaba', 1, 100)

enemy2.add_move(Attack(1, 10, 100))
enemy2.add_move(Attack(1, 10, 100))
enemy2.add_move(Attack(1, 20, 50))
enemy2.add_move(Defend(1, 10, 90))
enemy2.add_move(Defend(1, 10, 90))
enemy2.add_move(Heal(1, 30, 40))
enemy2.inventory.add_item(Item('kir-sag', 10))

enemies = [enemy1, enemy2]

Dungeon(player, enemies).start()

print(player.inventory)