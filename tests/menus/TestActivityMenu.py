from unittest.mock import Mock, patch

from src.menus.ActivityMenu import ActivityMenu


class TestActivityMenu:
    def test_open_returns_false_for_exit(self):
        with patch("builtins.input", return_value="exit"), patch("builtins.print"):
            assert ActivityMenu(Mock()).open() is False

    def test_open_retries_invalid_input_before_opening_selected_menu(self):
        player = Mock()
        menu = Mock()
        menu.return_value.open.return_value = False
        with patch.object(ActivityMenu, "menus", [menu]), \
             patch("builtins.input", side_effect=["bad", "4", "0"]), \
             patch("builtins.print"):
            result = ActivityMenu(player).open()
        assert result is True
        menu.assert_called_once_with(player)
        menu.return_value.open.assert_called_once_with()
