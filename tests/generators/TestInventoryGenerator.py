import pytest

from src.generators.InventoryGenerator import InventoryGenerator


class TestInventoryGenerator:
    def test_generate_rejects_rank_below_one(self):
        with pytest.raises(ValueError):
            InventoryGenerator.generate(0)

    def test_generate_adds_two_items_per_rank_and_rank_scaled_coins(self):
        from src.things.Item import Item
        from unittest.mock import patch

        generated = [Item("item-a", 5), Item("item-b", 5), Item("item-c", 5), Item("item-d", 5)]
        with patch("src.generators.InventoryGenerator.ItemGenerator.generate", side_effect=generated):
            inventory = InventoryGenerator.generate(2)

        assert inventory.exist_item("item-a")
        assert inventory.exist_item("item-b")
        assert inventory.exist_item("item-c")
        assert inventory.exist_item("item-d")
        assert inventory.get()["coin"] == 20

    def test_generate_rank_one_coin_count(self):
        from src.things.Item import Item
        from unittest.mock import patch

        with patch("src.generators.InventoryGenerator.ItemGenerator.generate", return_value=Item("iron", 5)):
            inventory = InventoryGenerator.generate(1)
        assert inventory.get()["coin"] == 15
