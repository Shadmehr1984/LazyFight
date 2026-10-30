from src.moves.MoveTarget import MoveTarget


class TestMoveTarget:
    def test_myself_target_value(self):
        assert MoveTarget.myself.value == "myself"

    def test_opponent_target_value(self):
        assert MoveTarget.opponent.value == "opponent"

    def test_targets_are_distinct_enum_members(self):
        assert MoveTarget.myself is not MoveTarget.opponent
        assert list(MoveTarget) == [MoveTarget.myself, MoveTarget.opponent]
