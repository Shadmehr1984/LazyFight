from unittest.mock import Mock, patch

import pytest

from src.chests.MoveChest import MoveChest
from src.chests.exceptions.ChestAndMovesRankNotSameException import ChestAndMovesRankNotSameException
from src.chests.exceptions.NotEnoughCoinException import NotEnoughCoinException
from src.chests.exceptions.NotEnoughMovesForChestException import NotEnoughMovesForChestException
from src.moves.Move import Move


def make_moves(rank=1):
    return [Move(rank, 10, 80, {}) for _ in range(3)]


class TestMoveChest:
    def test_init_sets_rank_moves_and_price(self):
        moves = make_moves()
        chest = MoveChest(1, moves)
        assert chest.rank == 1
        assert chest.moves is moves
        assert chest.price == 150

    def test_init_rejects_invalid_rank(self):
        with pytest.raises(ValueError):
            MoveChest(0, make_moves())

    def test_init_requires_three_moves(self):
        with pytest.raises(NotEnoughMovesForChestException):
            MoveChest(1, make_moves()[:2])

    def test_init_requires_matching_move_ranks(self):
        moves = make_moves()
        moves[-1].rank = 2
        with pytest.raises(ChestAndMovesRankNotSameException):
            MoveChest(1, moves)

    def test_open_returns_random_move_when_payment_succeeds(self):
        moves = make_moves()
        chest = MoveChest(1, moves)
        inventory = Mock()
        inventory.pick_item.return_value = True
        with patch("src.chests.MoveChest.randint", return_value=2):
            result = chest.open(inventory)
        inventory.pick_item.assert_called_once_with("coin", 150)
        assert result is moves[2]

    def test_open_translates_payment_errors_to_not_enough_coin(self):
        chest = MoveChest(1, make_moves())
        inventory = Mock()
        inventory.pick_item.side_effect = ValueError("not enough")
        inventory.items = {}
        with pytest.raises(NotEnoughCoinException, match="your coins:0"):
            chest.open(inventory)

    def test_string_representation(self):
        assert str(MoveChest(2, make_moves(2))) == "move chest, rank:2, price:250"
