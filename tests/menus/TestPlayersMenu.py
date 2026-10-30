from unittest.mock import Mock, patch

from src.menus.PlayersMenu import PlayersMenu


class TestPlayersMenu:
    def test_open_returns_false_for_exit(self):
        with patch("builtins.input", return_value="exit"), patch("builtins.print"):
            assert PlayersMenu([]).open() is False

    def test_open_selects_player_and_opens_activity_menu(self):
        player = Mock()
        activity_menu = Mock()
        activity_menu.return_value.open.return_value = False
        with patch("builtins.input", return_value="0"), \
             patch("src.menus.PlayersMenu.ActivityMenu", activity_menu), \
             patch("builtins.print"):
            result = PlayersMenu([player]).open()
        assert result is True
        activity_menu.assert_called_once_with(player)
