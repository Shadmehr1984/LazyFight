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
