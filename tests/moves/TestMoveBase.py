from unittest.mock import Mock, patch

import pytest

from src.moves.Move import Move


class TestMove:
    def test_init_stores_move_attributes(self):
        requirements = {"coin": 2, "gem": 1}

        move = Move(rank=1, value=10, accurate=75, rank_up_require=requirements)

        assert move.move_id is None
        assert move.rank == 1
        assert move.value == 10
        assert move.accurate == 75
        assert move.rank_up_require is requirements
        assert move.rate == 1

    @pytest.mark.parametrize(
        ("exception",),
        [(IndexError,), (ValueError,)],
    )
    def test_rank_up_returns_false_when_inventory_cannot_pay(self, exception):
        move = Move(rank=1, value=10, accurate=70, rank_up_require={"coin": 2})
        inventory = Mock()
        inventory.pick_items.side_effect = exception("cannot pay")

        result = move.rank_up(inventory)

        assert result is False
        assert move.rank == 1
        assert move.value == 10
        assert move.accurate == 70
        assert move.rank_up_require == {"coin": 2}

    def test_rank_up_updates_rank_value_accuracy_and_requirements(self):
        move = Move(rank=1, value=20, accurate=70, rank_up_require={"coin": 2, "gem": 1})
        inventory = Mock()

        result = move.rank_up(inventory)

        inventory.pick_items.assert_called_once_with({"coin": 2, "gem": 1})
        assert result is None
        assert move.rank == 2
        assert move.value == 21
        assert move.accurate == 72
        assert move.rank_up_require == {"coin": 3, "gem": 2}

    def test_rank_up_does_not_raise_accuracy_above_100(self):
        move = Move(rank=1, value=20, accurate=100, rank_up_require={})

        move.rank_up(Mock())

        assert move.accurate == 100

    @pytest.mark.parametrize(("random_value", "expected"), [(0, True), (70, True), (71, False), (100, False)])
    def test_move_take_uses_accuracy_threshold(self, random_value, expected):
        move = Move(rank=1, value=10, accurate=70, rank_up_require={})

        with patch("src.moves.Move.randint", return_value=random_value) as randint_mock:
            move.move_take()

        randint_mock.assert_called_once_with(0, 100)
        assert move.is_take is expected

    def test_is_effected_adds_move_when_it_hits(self):
        move = Move(rank=1, value=10, accurate=70, rank_up_require={})
        move.is_take = True
        owner = Mock()

        move.is_effected(owner)

        owner.add_effected_move.assert_called_once_with(move)

    def test_is_effected_adds_none_when_it_misses(self):
        move = Move(rank=1, value=10, accurate=70, rank_up_require={})
        move.is_take = False
        owner = Mock()

        move.is_effected(owner)

        owner.add_effected_move.assert_called_once_with(None)
