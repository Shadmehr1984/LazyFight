import pytest

from src.creatures.Creature import Creature
from src.creatures.Group import Group
from src.creatures.exceptions.NameIsToBigException import NameIsToBigException
from src.creatures.exceptions.NameIsToSmallException import NameIsToSmallException


class DummyMove:
    def __init__(self, rate=1):
        self.rate = rate


class DummyAttack(DummyMove):
    pass


class TestCreature:
    def test_initial_creature(self):
        creature = Creature("Raven", 2, Group.rock, 100)

        assert creature.name == "Raven"
        assert creature.rank == 2
        assert creature.group == Group.rock
        assert creature.max_hp == 100
        assert creature.current_hp == 100
        assert creature.base_defense == 10
        assert creature.defense == 0
        assert creature.group_rate == 1
        assert creature.inventory is not None
        assert creature.moves == []
        assert creature.fight_moves == []
        assert creature.turn_moves == []
        assert creature.effected_moves == []

    def test_name_too_short_raises_exception(self):
        with pytest.raises(NameIsToSmallException):
            Creature("Fox", 1, Group.rock, 50)

    def test_name_too_long_raises_exception(self):
        with pytest.raises(NameIsToBigException):
            Creature("LongCreature", 1, Group.rock, 50)

    def test_name_boundaries_are_valid(self):
        assert Creature("Wolf", 1, Group.rock, 50).name == "Wolf"
        assert Creature("Dragonxx", 1, Group.rock, 50).name == "Dragonxx"

    def test_add_move(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        move = DummyMove()

        creature.add_move(move)

        assert creature.moves == [move]

    def test_add_effected_move(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        move = DummyMove()

        creature.add_effected_move(move)
        creature.add_effected_move(None)

        assert creature.effected_moves == [move, None]

    def test_clear_fight_moves(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        creature.fight_moves = [DummyMove(), DummyMove()]

        creature.clear_fight_moves()

        assert creature.fight_moves == []

    def test_clear_turn_moves(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        creature.turn_moves = [DummyMove()]

        creature.clear_turn_moves()

        assert creature.turn_moves == []

    def test_clear_effected_moves(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        creature.effected_moves = [DummyMove(), None]

        creature.clear_effected_moves()

        assert creature.effected_moves == []

    def test_set_base_defense(self):
        creature = Creature("Raven", 1, Group.rock, 100)

        creature.set_base_defense(25)

        assert creature.base_defense == 25

    def test_reset_restores_hp_defense_and_clears_selected_moves(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        creature.current_hp = 30
        creature.base_defense = 18
        creature.defense = 2
        creature.fight_moves = [DummyMove()]
        creature.turn_moves = [DummyMove()]
        creature.effected_moves = [DummyMove()]

        creature.reset()

        assert creature.current_hp == 100
        assert creature.defense == 18
        assert creature.fight_moves == []
        assert creature.turn_moves == []
        assert creature.effected_moves == []

    def test_set_moves_rate_only_changes_exact_matching_class(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        attack = DummyAttack()
        base_move = DummyMove()
        creature.moves = [attack, base_move]

        creature.set_moves_rate(0.5, DummyAttack)

        assert attack.rate == 1.5
        assert base_move.rate == 1

    def test_reset_moves_rate_sets_all_moves_to_one(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        first = DummyMove(2.5)
        second = DummyMove(0.25)
        creature.moves = [first, second]

        creature.reset_moves_rate()

        assert first.rate == 1
        assert second.rate == 1

    @pytest.mark.parametrize(
        ("own_group", "opponent_group", "expected_rate"),
        [
            (Group.rock, Group.scissor, 1.1),
            (Group.rock, Group.rock, 1),
            (Group.rock, Group.paper, 0.9),
        ],
    )
    def test_set_group_rate(self, own_group, opponent_group, expected_rate):
        creature = Creature("Raven", 1, own_group, 100)

        creature.set_group_rate(opponent_group)

        assert creature.group_rate == expected_rate

    def test_reset_group_rate(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        creature.group_rate = 1.1

        creature.reset_group_rate()

        assert creature.group_rate == 1

    def test_take_damage_uses_defense_before_hp(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        creature.defense = 10

        creature.take_damage(6)

        assert creature.defense == 4
        assert creature.current_hp == 100

    def test_take_damage_reduces_hp_after_defense_is_exhausted(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        creature.defense = 5

        creature.take_damage(12)

        assert creature.defense == 0
        assert creature.current_hp == 93

    def test_get_defend_applies_group_rate(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        creature.group_rate = 1.1

        creature.get_defend(10)

        assert creature.defense == 11

    def test_get_heal_applies_group_rate(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        creature.current_hp = 50
        creature.group_rate = 1.1

        creature.get_heal(10)

        assert creature.current_hp == 61

    def test_get_heal_does_not_exceed_max_hp(self):
        creature = Creature("Raven", 1, Group.rock, 100)
        creature.current_hp = 95

        creature.get_heal(10)

        assert creature.current_hp == 100

    def test_str(self):
        creature = Creature("Raven", 3, Group.paper, 100)
        creature.current_hp = 75
        creature.defense = 12

        assert str(creature) == "Raven, group:paper, rank:3, hp:75, defense:12"
