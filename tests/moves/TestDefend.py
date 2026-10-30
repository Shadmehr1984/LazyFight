from src.moves.Defend import Defend
from src.moves.MoveTarget import MoveTarget


class TestDefend:
    def test_initial_defend_values(self):
        defend = Defend(2, 30, 85, {'stone': 2})

        assert defend.rank == 2
        assert defend.value == 30
        assert defend.accurate == 85
        assert defend.rank_up_require == {'stone': 2}
        assert defend.move_target == MoveTarget.myself

    def test_effect_increases_owner_defense_when_move_hits(self):
        defend = Defend(1, 25, 90, {})
        defend.is_take = True

        class Owner:
            def __init__(self):
                self.defense_gained = []

            def get_defend(self, value):
                self.defense_gained.append(value)

        owner = Owner()
        defend.effect(owner)

        assert owner.defense_gained == [25]

    def test_effect_does_not_increase_defense_when_move_misses(self):
        defend = Defend(1, 25, 90, {})
        defend.is_take = False

        class Owner:
            def __init__(self):
                self.defense_gained = []

            def get_defend(self, value):
                self.defense_gained.append(value)

        owner = Owner()
        defend.effect(owner)

        assert owner.defense_gained == []

    def test_effect_applies_rate_and_converts_defense_to_integer(self):
        defend = Defend(1, 25, 90, {})
        defend.is_take = True
        defend.rate = 1.5

        class Owner:
            def __init__(self):
                self.defense_gained = []

            def get_defend(self, value):
                self.defense_gained.append(value)

        owner = Owner()
        defend.effect(owner)

        assert owner.defense_gained == [37]

    def test_string_representation(self):
        defend = Defend(3, 42, 90, {'stone': 2})

        assert str(defend) == 'defend, rank:3, value:42, accurate:90'
