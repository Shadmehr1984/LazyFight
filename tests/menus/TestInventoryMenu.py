from unittest.mock import Mock, patch

from src.menus.InventoryMenu import InventoryMenu


class TestInventoryMenu:
    def test_open_reports_empty_inventory(self):
        player = Mock()
        player.name = "Ada"
        player.inventory.len.return_value = 0
        with patch("builtins.input", return_value=""), patch("builtins.print") as printer:
            result = InventoryMenu(player).open()
        assert result is None
        assert any("inventory is empty" in str(call) for call in printer.call_args_list)

    def test_open_prints_nonempty_inventory(self):
        player = Mock()
        player.name = "Ada"
        player.inventory.len.return_value = 1
        with patch("builtins.input", return_value=""), patch("builtins.print") as printer:
            InventoryMenu(player).open()
        player.inventory.__str__.assert_not_called()
        assert printer.call_count > 0
