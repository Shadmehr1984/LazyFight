from unittest.mock import patch

from src.menus.MainMenu import MainMenu


class TestMainMenu:
    def test_open_returns_for_exit(self):
        with patch("builtins.input", return_value="exit"), patch("builtins.print"):
            assert MainMenu([]).open() is None

    def test_show_menus_lists_create_and_select_options(self):
        with patch("builtins.print") as printer:
            MainMenu([])._MainMenu__show_menus()
        output = " ".join(str(call.args[0]) for call in printer.call_args_list)
        assert "create new player" in output
        assert "select a player" in output
