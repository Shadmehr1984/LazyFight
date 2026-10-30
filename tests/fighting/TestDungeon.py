from unittest.mock import Mock, call, patch

from src.fighting.Dungeon import Dungeon
from src.things.Inventory import Inventory
from src.things.Item import Item


def make_inventory(item_name: str, count: int = 1) -> Inventory:
    inventory = Inventory()
    inventory.add_item(Item(item_name, count))
    return inventory


class TestDungeon:
    def test_init_collects_enemy_inventories(self):
        player = Mock(inventory=Inventory())
        enemies = [
            Mock(inventory=make_inventory("iron", 2)),
            Mock(inventory=make_inventory("wood", 3)),
        ]

        dungeon = Dungeon(player, enemies)

        assert dungeon.player is player
        assert dungeon.enemies is enemies
        assert dungeon.inventory.get() == {"iron": 2, "wood": 3}

    def test_start_returns_false_and_resets_player_when_fight_is_lost(self):
        player = Mock(inventory=Inventory())
        enemy = Mock(inventory=make_inventory("iron", 2))

        with patch("src.fighting.Dungeon.Fight") as fight_class, \
             patch("src.fighting.Dungeon.Dungeon.save") as save, \
             patch("builtins.print"):
            fight_class.return_value.start.return_value = False
            dungeon = Dungeon(player, [enemy])

            result = dungeon.start()

        assert result is False
        player.reset.assert_called_once()
        player.inventory.add_all_inventory.assert_not_called()
        save.assert_not_called()
        fight_class.assert_called_once_with(player, enemy)

    def test_start_stops_after_first_lost_fight(self):
        player = Mock(inventory=Inventory())
        enemies = [
            Mock(inventory=make_inventory("iron")),
            Mock(inventory=make_inventory("wood")),
        ]

        with patch("src.fighting.Dungeon.Fight") as fight_class, \
             patch("src.fighting.Dungeon.Dungeon.save") as save, \
             patch("builtins.print"):
            fight_class.return_value.start.return_value = False
            dungeon = Dungeon(player, enemies)

            result = dungeon.start()

        assert result is False
        assert fight_class.call_args_list == [call(player, enemies[0])]
        player.reset.assert_called_once()
        save.assert_not_called()

    def test_start_rewards_inventory_resets_and_saves_on_win(self):
        player_inventory = Inventory()
        player_inventory.add_item(Item("coin", 5))
        player = Mock(inventory=player_inventory)
        enemies = [
            Mock(inventory=make_inventory("iron", 2)),
            Mock(inventory=make_inventory("wood", 3)),
        ]

        with patch("src.fighting.Dungeon.Fight") as fight_class, \
             patch("src.fighting.Dungeon.Dungeon.save") as save, \
             patch("builtins.print"):
            fight_class.return_value.start.return_value = True
            dungeon = Dungeon(player, enemies)

            result = dungeon.start()

        assert result is True
        assert fight_class.call_args_list == [
            call(player, enemies[0]),
            call(player, enemies[1]),
        ]
        assert player.inventory.get() == {"coin": 5, "iron": 2, "wood": 3}
        player.reset.assert_called_once()
        save.assert_called_once_with(dungeon)
