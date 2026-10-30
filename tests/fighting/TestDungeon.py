from unittest.mock import Mock, patch

from src.fighting.Dungeon import Dungeon


class TestDungeon:
    def test_init_collects_enemy_inventories(self):
        player = Mock()
        enemies = [Mock(), Mock()]
        dungeon = Dungeon(player, enemies)
        assert dungeon.player is player
        assert dungeon.enemies is enemies
        assert dungeon.inventory.add_all_inventory.call_count == 2

    def test_start_returns_false_and_resets_player_when_fight_is_lost(self):
        player = Mock()
        enemy = Mock()
        with patch("src.fighting.Dungeon.Fight") as fight_class, patch("builtins.print"):
            fight_class.return_value.start.return_value = False
            dungeon = Dungeon(player, [enemy])
            result = dungeon.start()
        assert result is False
        player.reset.assert_called_once()

    def test_start_rewards_inventory_resets_and_saves_on_win(self):
        player = Mock()
        enemies = [Mock(), Mock()]
        with patch("src.fighting.Dungeon.Fight") as fight_class, \
             patch("src.fighting.Dungeon.Dungeon.save") as save, \
             patch("builtins.print"):
            fight_class.return_value.start.return_value = True
            dungeon = Dungeon(player, enemies)
            result = dungeon.start()
        assert result is True
        player.inventory.add_all_inventory.assert_called_once_with(dungeon.inventory)
        player.reset.assert_called_once()
        save.assert_called_once_with(dungeon)
