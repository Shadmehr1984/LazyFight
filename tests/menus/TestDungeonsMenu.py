from unittest.mock import Mock, patch

from src.menus.DungeonsMenu import DungeonsMenu


class TestDungeonsMenu:
    def test_open_returns_false_for_exit(self):
        player = Mock()
        player.rank = 3
        with patch("builtins.input", return_value="exit"), patch("builtins.print"):
            assert DungeonsMenu(player).open() is False

    def test_generate_dungeon_delegates_to_generator(self):
        player = Mock()
        dungeon = Mock()
        with patch("src.menus.DungeonsMenu.DungeonGenerator.generate", return_value=dungeon) as generate:
            result = DungeonsMenu(player)._DungeonsMenu__generate_dungeon(2)
        generate.assert_called_once_with(2, player)
        assert result is dungeon
