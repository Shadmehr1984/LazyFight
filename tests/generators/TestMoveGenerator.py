import pytest

from src.generators.MoveGenerator import MoveGenerator
from src.moves.Attack import Attack
from src.moves.Buff import Buff
from src.moves.Defend import Defend
from src.moves.Heal import Heal
from src.moves.Nerf import Nerf


@pytest.mark.parametrize(
    ("move_type", "expected_class", "expected_value", "expected_accuracy"),
    [
        ("attack", Attack, 10, 100),
        ("defend", Defend, 10, 90),
        ("heal", Heal, 20, 20),
        ("buff", Buff, 0.10, 70),
        ("nerf", Nerf, 0.10, 70),
    ],
)
def test_generate_rank_one_move(move_type, expected_class, expected_value, expected_accuracy):
    if move_type in ("buff", "nerf"):
        move = MoveGenerator.generate(1, move_type, "attack")
        assert move.move_class is Attack
    else:
        move = MoveGenerator.generate(1, move_type)

    assert isinstance(move, expected_class)
    assert move.rank == 1
    assert move.value == expected_value
    assert move.accurate == expected_accuracy
    assert move.move_id is None


@pytest.mark.parametrize("rank", [0, -1])
def test_generate_rejects_non_positive_rank(rank):
    with pytest.raises(ValueError):
        MoveGenerator.generate(rank, "attack")


@pytest.mark.parametrize("move_type", ["", "invalid", "ATTACK", None])
def test_generate_rejects_unknown_move_type(move_type):
    with pytest.raises(ValueError):
        MoveGenerator.generate(1, move_type)


@pytest.mark.parametrize("move_type", ["buff", "nerf"])
@pytest.mark.parametrize("target", [None, "", "invalid", "Attack"])
def test_generate_rejects_invalid_buff_or_nerf_target(move_type, target):
    with pytest.raises(ValueError):
        MoveGenerator.generate(1, move_type, target)


@pytest.mark.parametrize(
    ("target", "expected_class"),
    [("attack", Attack), ("defend", Defend), ("heal", Heal)],
)
@pytest.mark.parametrize("move_type", ["buff", "nerf"])
def test_generate_buff_and_nerf_target_classes(move_type, target, expected_class):
    move = MoveGenerator.generate(1, move_type, target)
    assert move.move_class is expected_class


def test_generate_rank_two_attack_calculates_ranked_stats_without_mutating_base_requirements(monkeypatch):
    monkeypatch.setattr(Attack, "_Attack__BASE_RANK_UP_REQUIRE", {"fire-token": 5, "iron": 5})

    move = MoveGenerator.generate(2, "attack")

    assert move.value == 11
    assert move.accurate == 100
    assert move.rank_up_require == {"fire-token": 8, "iron": 8}
    assert Attack._Attack__BASE_RANK_UP_REQUIRE == {"fire-token": 5, "iron": 5}


def test_generate_rank_two_buff_uses_fractional_rank_value(monkeypatch):
    monkeypatch.setattr(Buff, "_Buff__BASE_RANK_UP_REQUIRE", {"light-token": 15, "glass": 20})

    move = MoveGenerator.generate(2, "buff", "defend")

    assert move.value == pytest.approx(0.2)
    assert move.accurate == 72
    assert move.rank_up_require == {"light-token": 23, "glass": 30}
    assert Buff._Buff__BASE_RANK_UP_REQUIRE == {"light-token": 15, "glass": 20}


def test_calculate_accuracy_caps_at_one_hundred():
    assert MoveGenerator._MoveGenerator__calculate_accurate(10, 99) == 100


@pytest.mark.parametrize(
    ("rank", "base", "expected"),
    [
        (1, {"iron": 5}, {"iron": 5}),
        (2, {"iron": 5}, {"iron": 8}),
        (3, {"iron": 5}, {"iron": 8}),
    ],
)
def test_calculate_rank_up_require(rank, base, expected):
    # The method mutates its input, so each case receives its own dictionary.
    result = MoveGenerator._MoveGenerator__calculate_rank_up_require(rank, base)
    assert result == expected
