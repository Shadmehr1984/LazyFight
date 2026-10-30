from unittest.mock import Mock, patch

import pytest

from src.chests.ItemChest import ItemChest
from src.chests.exceptions.NotEnoughCoinException import NotEnoughCoinException
from src.chests.exceptions.NotEnoughItemsForChestException import NotEnoughItemsForChestException
from src.chests.exceptions.NotValidItemCountException import NotValidItemCountException
from src.things.Item import Item


class TestItemChest:
    def test_init_sets_rank_items_and_price(self):
        items = [Item("iron", 5), Item("wood", 5), Item("stone", 5)]
        chest = ItemChest(1, items)
        assert chest.rank == 1
        assert chest.items is items
        assert chest.price == 70

    def test_init_rejects_invalid_rank(self):
        with pytest.raises(ValueError):
            ItemChest(0, [Item("iron", 5)] * 3)

    def test_init_requires_at_least_three_items(self):
        with pytest.raises(NotEnoughItemsForChestException):
            ItemChest(1, [Item("iron", 5), Item("wood", 5)])

    def test_init_requires_item_count_to_match_rank(self):
        with pytest.raises(NotValidItemCountException):
            ItemChest(2, [Item("iron", 10), Item("wood", 9), Item("stone", 10)])

    def test_open_returns_random_item_when_payment_succeeds(self):
        items = [Item("iron", 5), Item("wood", 5), Item("stone", 5)]
        chest = ItemChest(1, items)
        inventory = Mock()
        inventory.pick_item.return_value = True
        with patch("src.chests.ItemChest.randint", return_value=1):
            result = chest.open(inventory)
        inventory.pick_item.assert_called_once_with("coin", 70)
        assert result is items[1]

    def test_open_translates_payment_errors_to_not_enough_coin(self):
        chest = ItemChest(1, [Item("iron", 5), Item("wood", 5), Item("stone", 5)])
        inventory = Mock()
        inventory.pick_item.side_effect = ValueError("not enough")
        inventory.items = {}
        with pytest.raises(NotEnoughCoinException, match="your coins:0"):
            chest.open(inventory)

    def test_string_representation(self):
        chest = ItemChest(2, [Item("iron", 10), Item("wood", 10), Item("stone", 10)])
        assert str(chest) == "item chest, rank:2, price:90"
