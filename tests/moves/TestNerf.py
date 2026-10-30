import pytest

from src.moves.Attack import Attack
from src.moves.Defend import Defend
from src.moves.Heal import Heal
from src.moves.MoveTarget import MoveTarget
from src.moves.Nerf import Nerf


class TestNerf:
    def test_initial_nerf_values(self):
        nerf = Nerf(2, 0.2, 85, Attack, {"dark-token": 15})

        assert nerf.rank == 2
        assert nerf.value == 0.2
        assert nerf.accurate == 85
        assert nerf.rank_up_require == {"dark-token": 15}
        assert nerf.move_class is Attack
        assert nerf.move_target == MoveTarget.opponent

    def test_negative_value_is_rejected(self):
        with pytest.raises(ValueError, match="value must be greater or equal 0"):
            Nerf(1, -0.1, 70, Attack, {})

    @pytest.mark.parametrize("move_class", [str, object, None])
    def test_invalid_move_class_is_rejected(self, move_class):
        with pytest.raises(ValueError, match="move_class must be type of Attack, Defend or Heal"):
            Nerf(1, 0.1, 70, move_class, {})

    @pytest.mark.parametrize("move_class", [Attack, Defend, Heal])
    def test_effect_applies_negative_rate_when_move_hits(self, move_class):
        nerf = Nerf(1, 0.25, 100, move_class, {})
        nerf.is_take = True

        class Opponent:
            def __init__(self):
                self.applied_rates = []

            def set_moves_rate(self, value, target_class):
                self.applied_rates.append((value, target_class))

        opponent = Opponent()
        nerf.effect(opponent)

        assert opponent.applied_rates == [(-0.25, move_class)]

    def test_effect_does_nothing_when_move_misses(self):
        nerf = Nerf(1, 0.25, 100, Attack, {})
        nerf.is_take = False

        class Opponent:
            def __init__(self):
                self.applied_rates = []

            def set_moves_rate(self, value, target_class):
                self.applied_rates.append((value, target_class))

        opponent = Opponent()
        nerf.effect(opponent)

        assert opponent.applied_rates == []

    def test_rank_up_updates_nerf_stats_and_requirements(self):
        nerf = Nerf(1, 0.2, 70, Attack, {"dark-token": 15, "oil": 20})

        class InventoryStub:
            def pick_items(self, requirements):
                self.requirements = requirements

        result = nerf.rank_up(InventoryStub())

        assert result is None
        assert nerf.rank == 2
        assert nerf.value == pytest.approx(0.3)
        assert nerf.accurate == 72
        assert nerf.rank_up_require == {"dark-token": 23, "oil": 30}

    @pytest.mark.parametrize("error", [IndexError, ValueError])
    def test_rank_up_returns_false_when_inventory_cannot_supply_items(self, error):
        nerf = Nerf(1, 0.2, 70, Attack, {"dark-token": 15})

        class InventoryStub:
            def pick_items(self, requirements):
                raise error("not enough items")

        result = nerf.rank_up(InventoryStub())

        assert result is False
        assert nerf.rank == 1
        assert nerf.value == 0.2
        assert nerf.accurate == 70
        assert nerf.rank_up_require == {"dark-token": 15}

    def test_rank_up_caps_accuracy_at_100(self):
        nerf = Nerf(1, 0.2, 99, Heal, {})

        class InventoryStub:
            def pick_items(self, requirements):
                pass

        nerf.rank_up(InventoryStub())

        assert nerf.accurate == 100

    def test_string_representation(self):
        nerf = Nerf(3, 0.4, 90, Defend, {"oil": 2})

        assert str(nerf) == "nerf, rank:3, value:0.4, accurate:90, move class:Defend"
