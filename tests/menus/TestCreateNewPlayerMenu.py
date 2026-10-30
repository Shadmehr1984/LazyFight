from unittest.mock import Mock, patch

from src.creatures.Group import Group
from src.menus.CreateNewPlayerMenu import CreateNewPlayerMenu


class TestCreateNewPlayerMenu:
    def test_open_creates_player_with_selected_group_and_saves(self):
        generated_moves = [Mock() for _ in range(6)]
        enemy = Mock()
        enemy.moves = generated_moves
        with patch("builtins.input", side_effect=["Adamss", "rock"]), \
             patch("src.menus.CreateNewPlayerMenu.EnemyGenerator.generate", return_value=enemy) as generate_enemy, \
             patch("src.menus.CreateNewPlayerMenu.PlayerModel") as player_model:
            player = CreateNewPlayerMenu([]).open()
        assert player.name == "Adamss"
        assert player.group == Group.rock
        assert len(player.moves) == 6
        generate_enemy.assert_called_once_with(1, "rrrrrr", "rock")
        player_model.assert_called_once_with(player)
        player_model.return_value.save.assert_called_once_with()

    def test_open_rejects_duplicate_name_then_accepts_new_name(self):
        existing_player = Mock()
        existing_player.name = "Ada"
        enemy = Mock()
        enemy.moves = [Mock() for _ in range(6)]
        with patch("builtins.input", side_effect=["Ada", "Luna", "paper"]), \
             patch("src.menus.CreateNewPlayerMenu.EnemyGenerator.generate", return_value=enemy), \
             patch("src.menus.CreateNewPlayerMenu.PlayerModel"), patch("builtins.print"):
            player = CreateNewPlayerMenu([existing_player]).open()
        assert player.name == "Luna"
        assert player.group == Group.paper
