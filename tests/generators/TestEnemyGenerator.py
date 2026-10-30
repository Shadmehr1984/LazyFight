import pytest

from src.generators.EnemyGenerator import EnemyGenerator
from src.creatures.Group import Group


class TestEnemyGenerator:
    def test_generate_rejects_invalid_rank(self):
        with pytest.raises(ValueError):
            EnemyGenerator.generate(0, "enemy", "rock")

    def test_generate_rejects_invalid_group(self):
        with pytest.raises(ValueError):
            EnemyGenerator.generate(1, "enemy", "invalid")

    @pytest.mark.parametrize(("group_name", "expected_group"), [
        ("rock", Group.rock), ("paper", Group.paper), ("scissor", Group.scissor)
    ])
    def test_generate_builds_enemy_with_expected_stats_and_moves(self, group_name, expected_group):
        enemy = EnemyGenerator.generate(1, "enemy", group_name)
        assert enemy.name == "enemy"
        assert enemy.rank == 1
        assert enemy.group == expected_group
        assert enemy.max_hp == 100
        assert enemy.base_defense == 10
        assert len(enemy.moves) == 6
        assert enemy.inventory.get()["coin"] == 15
