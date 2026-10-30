import pytest

from src.creatures.Group import Group


class TestGroup:
    def test_group_members(self):
        assert list(Group) == [Group.rock, Group.paper, Group.scissor]

    @pytest.mark.parametrize(
        ("group", "expected_value"),
        [
            (Group.rock, "rock"),
            (Group.paper, "paper"),
            (Group.scissor, "scissor"),
        ],
    )
    def test_group_values(self, group, expected_value):
        assert group.value == expected_value

    @pytest.mark.parametrize(
        ("self_group", "target_group", "expected_result"),
        [
            (Group.rock, Group.rock, 0),
            (Group.rock, Group.paper, -1),
            (Group.rock, Group.scissor, 1),
            (Group.paper, Group.rock, 1),
            (Group.paper, Group.paper, 0),
            (Group.paper, Group.scissor, -1),
            (Group.scissor, Group.rock, -1),
            (Group.scissor, Group.paper, 1),
            (Group.scissor, Group.scissor, 0),
        ],
    )
    def test_compare(self, self_group, target_group, expected_result):
        assert Group.compare(self_group, target_group) == expected_result
