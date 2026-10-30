from unittest.mock import Mock, patch

from src.menus.ChestMenu import ChestMenu


class TestChestMenu:
    def test_open_returns_false_for_exit(self):
        player = Mock()
        with patch.object(ChestMenu, "_ChestMenu__generate_chests", return_value=[]), \
             patch("builtins.input", return_value="exit"), patch("builtins.print"):
            assert ChestMenu(player).open() is False

    def test_generate_chests_creates_basic_move_and_item_chests(self):
        player = Mock()
        player.rank = 1
        with patch("src.menus.ChestMenu.ChestGenerator.generate", side_effect=["move-chest", "item-chest"]) as generate:
            result = ChestMenu(player)._ChestMenu__generate_chests()
        assert result == ["move-chest", "item-chest"]
        assert [call.args for call in generate.call_args_list] == [(1, "move"), (1, "item")]
