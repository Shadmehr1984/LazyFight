from unittest.mock import patch

import pytest

from src.chests.ItemChest import ItemChest
from src.chests.MoveChest import MoveChest
from src.generators.ChestGenerator import ChestGenerator


class TestChestGenerator:
    def test_generate_rejects_invalid_rank(self):
        with pytest.raises(ValueError):
            ChestGenerator.generate(0, "item")

    def test_generate_rejects_invalid_content(self):
        with pytest.raises(ValueError):
            ChestGenerator.generate(1, "unknown")

    def test_generate_item_chest(self):
        with patch("src.generators.ChestGenerator.ItemGenerator.generate") as generate_item:
            from src.things.Item import Item
            generate_item.side_effect = [Item("iron", 5), Item("wood", 5), Item("stone", 5)]
            chest = ChestGenerator.generate(1, "item")
        assert isinstance(chest, ItemChest)
        assert chest.rank == 1
        assert len(chest.items) == 3

    def test_generate_move_chest(self):
        with patch("src.generators.ChestGenerator.MoveGenerator.generate") as generate_move:
            from src.moves.Move import Move
            generate_move.return_value = Move(1, 10, 80, {})
            chest = ChestGenerator.generate(1, "move")
        assert isinstance(chest, MoveChest)
        assert chest.rank == 1
        assert len(chest.moves) == 3
        assert generate_move.call_count == 3
