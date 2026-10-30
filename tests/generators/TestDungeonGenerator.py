from unittest.mock import patch

import pytest

from src.fighting.Dungeon import Dungeon
from src.generators.DungeonGenerator import DungeonGenerator


class TestDungeonGenerator:
    def test_generate_rejects_invalid_rank(self):
        with pytest.raises(ValueError):
            DungeonGenerator.generate(0, object())

    def test_rank_one_generates_one_enemy(self):
        player = object()
        with patch("src.generators.DungeonGenerator.DungeonGenerator._DungeonGenerator__generate_random_group", return_value="rock"), \
             patch("src.generators.DungeonGenerator.RandomNameGenerator.generate", return_value="enemy"), \
             patch("src.generators.DungeonGenerator.EnemyGenerator.generate", return_value=object()) as enemy_generate, \
             patch("src.generators.DungeonGenerator.Dungeon") as dungeon_class:
            result = DungeonGenerator.generate(1, player)
        enemy_generate.assert_called_once_with(1, "enemy", "rock")
        dungeon_class.assert_called_once()
        assert result == dungeon_class.return_value

    def test_higher_rank_generates_triangular_enemy_count(self):
        with patch("src.generators.DungeonGenerator.DungeonGenerator._DungeonGenerator__generate_random_group", return_value="paper"), \
             patch("src.generators.DungeonGenerator.RandomNameGenerator.generate", return_value="enemy"), \
             patch("src.generators.DungeonGenerator.EnemyGenerator.generate", return_value=object()) as enemy_generate, \
             patch("src.generators.DungeonGenerator.Dungeon") as dungeon_class:
            result = DungeonGenerator.generate(3, object())
        assert enemy_generate.call_count == 6
        generated_enemies = dungeon_class.call_args.args[1]
        assert len(generated_enemies) == 6
        assert [call.args[0] for call in enemy_generate.call_args_list] == [1, 1, 1, 2, 2, 3]
