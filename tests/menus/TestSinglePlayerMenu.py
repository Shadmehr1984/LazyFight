import inspect

import pytest

from src.menus.SinglePlayerMenu import SinglePlayerMenu


class TestSinglePlayerMenu:
    def test_menu_is_abstract(self):
        assert inspect.isabstract(SinglePlayerMenu)
        with pytest.raises(TypeError):
            SinglePlayerMenu(object())

    def test_concrete_subclass_receives_player(self):
        class Menu(SinglePlayerMenu):
            def open(self):
                return False

        player = object()
        menu = Menu(player)
        assert menu.player is player
        assert menu.open() is False
