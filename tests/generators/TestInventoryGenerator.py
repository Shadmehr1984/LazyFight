import pytest

from src.generators.InventoryGenerator import InventoryGenerator


class TestInventoryGenerator:
    def test_generate_rejects_rank_below_one(self):
        with pytest.raises(ValueError):
            InventoryGenerator.generate(0)

    def test_generate_adds_two_random_items_per_rank_and_coins(self):
        inventory = InventoryGenerator.generate(2)
        assert len(inventory.items) == 5
        assert inventory.exist_item("coin")
        assert inventory.get()["coin"] == 20

    def test_generate_rank_one_coin_count(self):
        inventory = InventoryGenerator.generate(1)
        assert inventory.get()["coin"] == 15
