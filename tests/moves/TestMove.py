import pytest
from src.moves.Move import Move
from src.moves.MoveTarget import MoveTarget
from src.things.Inventory import Inventory
from src.things.Item import Item
from src.things.Exceptions.ItemNotEnoughException import ItemNotEnoughException
from src.things.Exceptions.ItemNotExistException import ItemNotExistException


class TestMove:
    def test_initial_move_values(self):
        move = Move(2, 30, 75, {'gold': 2})

        assert move.move_id is None
        assert move.rank == 2
        assert move.value == 30
        assert move.accurate == 75
        assert move.rank_up_require == {'gold': 2}
        assert move.rate == 1

    def test_move_target_enum_values(self):
        assert MoveTarget.myself.value == 'myself'
        assert MoveTarget.opponent.value == 'opponent'

    def test_rank_up_increases_rank_value_accuracy_and_requirements(self):
        move = Move(1, 20, 70, {'gold': 2, 'silver': 3})
        inventory = Inventory()
        inventory.add_item(Item('gold', 10))
        inventory.add_item(Item('silver', 10))

        move.rank_up(inventory)

        assert move.rank == 2
        assert move.value == 21
        assert move.accurate == 72
        assert move.rank_up_require == {'gold': 3, 'silver': 5}
        assert inventory.get() == {'gold': 8, 'silver': 7}

    def test_rank_up_does_not_increase_accuracy_above_100(self):
        move = Move(1, 10, 100, {'gold': 1})
        inventory = Inventory()
        inventory.add_item(Item('gold', 1))

        move.rank_up(inventory)

        assert move.accurate == 100

    def test_rank_up_caps_accuracy_at_100(self):
        move = Move(1, 10, 99, {'gold': 1})
        inventory = Inventory()
        inventory.add_item(Item('gold', 1))

        move.rank_up(inventory)

        assert move.accurate == 100

    def test_rank_up_with_missing_required_item_returns_false_without_changing_move(self):
        move = Move(1, 20, 70, {'gold': 2})
        inventory = Inventory()
        before = (move.rank, move.value, move.accurate, move.rank_up_require.copy())

        result = move.rank_up(inventory)

        assert result is False
        assert (move.rank, move.value, move.accurate, move.rank_up_require) == before

    def test_rank_up_with_insufficient_items_returns_false_without_changing_move(self):
        move = Move(1, 20, 70, {'gold': 3})
        inventory = Inventory()
        inventory.add_item(Item('gold', 1))
        before = (move.rank, move.value, move.accurate, move.rank_up_require.copy())

        result = move.rank_up(inventory)

        assert result is False
        assert (move.rank, move.value, move.accurate, move.rank_up_require) == before
        assert inventory.get() == {'gold': 1}

    def test_move_take_uses_accuracy_threshold(self, monkeypatch):
        move = Move(1, 10, 50, {})

        monkeypatch.setattr('src.moves.Move.randint', lambda lower, upper: 50)
        move.move_take()
        assert move.is_take is True

        monkeypatch.setattr('src.moves.Move.randint', lambda lower, upper: 51)
        move.move_take()
        assert move.is_take is False

    def test_is_effected_adds_move_when_it_hits(self):
        move = Move(1, 10, 50, {})
        move.is_take = True

        class MoveOwner:
            def __init__(self):
                self.effected_moves = []

            def add_effected_move(self, effected_move):
                self.effected_moves.append(effected_move)

        owner = MoveOwner()
        move.is_effected(owner)

        assert owner.effected_moves == [move]

    def test_is_effected_adds_none_when_it_misses(self):
        move = Move(1, 10, 50, {})
        move.is_take = False

        class MoveOwner:
            def __init__(self):
                self.effected_moves = []

            def add_effected_move(self, effected_move):
                self.effected_moves.append(effected_move)

        owner = MoveOwner()
        move.is_effected(owner)

        assert owner.effected_moves == [None]
