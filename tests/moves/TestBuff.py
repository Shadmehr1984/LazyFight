import pytest

from src.moves.Attack import Attack
from src.moves.Buff import Buff
from src.moves.Defend import Defend
from src.moves.Heal import Heal
from src.moves.MoveTarget import MoveTarget


class TestBuff:
    def test_initial_buff_values(self):
        buff = Buff(2, 0.2, 85, Attack, {"light-token": 15})

        assert buff.rank == 2
        assert buff.value == 0.2
        assert buff.accurate == 85
        assert buff.rank_up_require == {"light-token": 15}
        assert buff.move_class is Attack
        assert buff.move_target == MoveTarget.myself

    def test_negative_value_is_rejected(self):
        with pytest.raises(ValueError, match="value must be greater or equal 0"):
            Buff(1, -0.1, 70, Attack, {})

    @pytest.mark.parametrize("move_class", [str, object, None])
    def test_invalid_move_class_is_rejected(self, move_class):
        with pytest.raises(ValueError, match="move_class must be type of Attack, Defend or Heal"):
            Buff(1, 0.1, 70, move_class, {})

    @pytest.mark.parametrize("move_class", [Attack, Defend, Heal])
    def test_effect_applies_buff_when_move_hits(self, move_class):
        buff = Buff(1, 0.25, 100, move_class, {})
        buff.is_take = True

        class Owner:
            def __init__(self):
                self.applied_rates = []

            def set_moves_rate(self, value, target_class):
                self.applied_rates.append((value, target_class))

        owner = Owner()
        buff.effect(owner)

        assert owner.applied_rates == [(0.25, move_class)]

    def test_effect_does_nothing_when_move_misses(self):
        buff = Buff(1, 0.25, 100, Attack, {})
        buff.is_take = False

        class Owner:
            def __init__(self):
                self.applied_rates = []

            def set_moves_rate(self, value, target_class):
                self.applied_rates.append((value, target_class))

        owner = Owner()
        buff.effect(owner)

        assert owner.applied_rates == []

    def test_rank_up_updates_buff_stats_and_requirements(self):
        buff = Buff(1, 0.2, 70, Attack, {"light-token": 15, "glass": 20})

        class InventoryStub:
            def pick_items(self, requirements):
                self.requirements = requirements

        result = buff.rank_up(InventoryStub())

        assert result is None
        assert buff.rank == 2
        assert buff.value == pytest.approx(0.3)
        assert buff.accurate == 72
        assert buff.rank_up_require == {"light-token": 23, "glass": 30}

    @pytest.mark.parametrize("error", [IndexError, ValueError])
    def test_rank_up_returns_false_when_inventory_cannot_supply_items(self, error):
        buff = Buff(1, 0.2, 70, Attack, {"light-token": 15})

        class InventoryStub:
            def pick_items(self, requirements):
                raise error("not enough items")

        result = buff.rank_up(InventoryStub())

        assert result is False
        assert buff.rank == 1
        assert buff.value == 0.2
        assert buff.accurate == 70
        assert buff.rank_up_require == {"light-token": 15}

    def test_rank_up_caps_accuracy_at_100(self):
        buff = Buff(1, 0.2, 99, Heal, {})

        class InventoryStub:
            def pick_items(self, requirements):
                pass

        buff.rank_up(InventoryStub())

        assert buff.accurate == 100

    def test_string_representation(self):
        buff = Buff(3, 0.4, 90, Defend, {"glass": 2})

        assert str(buff) == "buff, rank:3, value:0.4, accurate:90, move class:Defend"
