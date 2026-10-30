from src.moves.Heal import Heal
from src.moves.MoveTarget import MoveTarget


class TestHeal:
    def test_initial_heal_values(self):
        heal = Heal(2, 30, 85, {'wood': 2})

        assert heal.rank == 2
        assert heal.value == 30
        assert heal.accurate == 85
        assert heal.rank_up_require == {'wood': 2}
        assert heal.move_target == MoveTarget.myself

    def test_effect_heals_owner_when_move_hits(self):
        heal = Heal(1, 25, 90, {})
        heal.is_take = True

        class Owner:
            def __init__(self):
                self.heal_received = []

            def get_heal(self, value):
                self.heal_received.append(value)

        owner = Owner()
        heal.effect(owner)

        assert owner.heal_received == [25]

    def test_effect_does_not_heal_owner_when_move_misses(self):
        heal = Heal(1, 25, 90, {})
        heal.is_take = False

        class Owner:
            def __init__(self):
                self.heal_received = []

            def get_heal(self, value):
                self.heal_received.append(value)

        owner = Owner()
        heal.effect(owner)

        assert owner.heal_received == []

    def test_effect_applies_rate_and_converts_heal_to_integer(self):
        heal = Heal(1, 25, 90, {})
        heal.is_take = True
        heal.rate = 1.5

        class Owner:
            def __init__(self):
                self.heal_received = []

            def get_heal(self, value):
                self.heal_received.append(value)

        owner = Owner()
        heal.effect(owner)

        assert owner.heal_received == [37]

    def test_string_representation(self):
        heal = Heal(3, 42, 90, {'wood': 2})

        assert str(heal) == 'heal, rank:3, value:42, accurate:90'
