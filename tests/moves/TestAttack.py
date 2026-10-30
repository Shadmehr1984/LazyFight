from src.moves.Attack import Attack
from src.moves.MoveTarget import MoveTarget


class TestAttack:
    def test_initial_attack_values(self):
        attack = Attack(2, 30, 85, {'iron': 2})

        assert attack.rank == 2
        assert attack.value == 30
        assert attack.accurate == 85
        assert attack.rank_up_require == {'iron': 2}
        assert attack.move_target == MoveTarget.opponent

    def test_effect_damages_opponent_when_attack_hits(self):
        attack = Attack(1, 25, 100, {})
        attack.is_take = True

        class Opponent:
            def __init__(self):
                self.damage_taken = []

            def take_damage(self, damage):
                self.damage_taken.append(damage)

        opponent = Opponent()
        attack.effect(opponent)

        assert opponent.damage_taken == [25]

    def test_effect_does_not_damage_opponent_when_attack_misses(self):
        attack = Attack(1, 25, 100, {})
        attack.is_take = False

        class Opponent:
            def __init__(self):
                self.damage_taken = []

            def take_damage(self, damage):
                self.damage_taken.append(damage)

        opponent = Opponent()
        attack.effect(opponent)

        assert opponent.damage_taken == []

    def test_effect_applies_rate_and_converts_damage_to_integer(self):
        attack = Attack(1, 25, 100, {})
        attack.is_take = True
        attack.rate = 1.5

        class Opponent:
            def __init__(self):
                self.damage_taken = []

            def take_damage(self, damage):
                self.damage_taken.append(damage)

        opponent = Opponent()
        attack.effect(opponent)

        assert opponent.damage_taken == [37]

    def test_string_representation(self):
        attack = Attack(3, 42, 90, {'iron': 2})

        assert str(attack) == 'attack, rank:3, value:42, accurate:90'
