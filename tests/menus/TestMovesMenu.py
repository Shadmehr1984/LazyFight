import pytest
from unittest.mock import Mock, patch

from src.menus.MovesMenu import MovesMenu


class TestMovesMenu:
    def test_open_returns_false_for_exit(self):
        player = Mock()
        player.moves = []
        with patch("builtins.input", return_value="exit"), patch("builtins.print"):
            assert MovesMenu(player).open() is False

    def test_show_moves_prints_index_and_move(self):
        move = Mock()
        player = Mock()
        player.moves = [move]
        with patch("builtins.print") as printer:
            MovesMenu(player)._MovesMenu__show_moves()
        assert printer.call_args.args[0].startswith("0:")

    @pytest.mark.parametrize("answer", ["N", "n"])
    def test_declining_rank_up_does_not_upgrade_or_save(self, answer):
        move = Mock()
        move.rank_up_require = {"coin": 2}
        inventory = Mock()
        inventory.exist_item.return_value = True
        inventory.enough_item.return_value = True
        player = Mock()
        player.moves = [move]
        player.inventory = inventory

        with patch("builtins.input", side_effect=["0", answer]), \
             patch("src.menus.MovesMenu.MoveModel") as model_class, \
             patch("builtins.print"):
            result = MovesMenu(player).open()

        assert result is True
        move.rank_up.assert_not_called()
        model_class.return_value.save.assert_not_called()

    def test_confirming_rank_up_upgrades_move_and_saves(self):
        move = Mock()
        move.rank_up_require = {"coin": 2}
        inventory = Mock()
        inventory.exist_item.return_value = True
        inventory.enough_item.return_value = True
        player = Mock()
        player.moves = [move]
        player.inventory = inventory

        with patch("builtins.input", side_effect=["0", "y"]), \
             patch("src.menus.MovesMenu.MoveModel") as model_class, \
             patch("builtins.print"):
            result = MovesMenu(player).open()

        assert result is True
        move.rank_up.assert_called_once_with(inventory)
        model_class.assert_called_once_with(player)
        model_class.return_value.save.assert_called_once_with()

    def test_open_returns_to_menu_when_required_item_is_missing(self):
        move = Mock()
        move.rank_up_require = {"coin": 2}
        inventory = Mock()
        inventory.exist_item.return_value = False
        player = Mock()
        player.moves = [move]
        player.inventory = inventory

        with patch("builtins.input", return_value="0"), \
             patch("src.menus.MovesMenu.MoveModel") as model_class, \
             patch("builtins.print"):
            result = MovesMenu(player).open()

        assert result is True
        inventory.enough_item.assert_not_called()
        move.rank_up.assert_not_called()
        model_class.return_value.save.assert_not_called()

    def test_open_returns_to_menu_when_required_item_count_is_insufficient(self):
        move = Mock()
        move.rank_up_require = {"coin": 2}
        inventory = Mock()
        inventory.exist_item.return_value = True
        inventory.enough_item.return_value = False
        inventory.get.return_value = {"coin": 1}
        player = Mock()
        player.moves = [move]
        player.inventory = inventory

        with patch("builtins.input", return_value="0"), \
             patch("src.menus.MovesMenu.MoveModel") as model_class, \
             patch("builtins.print"):
            result = MovesMenu(player).open()

        assert result is True
        inventory.enough_item.assert_called_once_with("coin", 2)
        move.rank_up.assert_not_called()
        model_class.return_value.save.assert_not_called()
