from unittest.mock import Mock, call

from src.fighting.Fight import Fight


class TestFight:
    def test_preparing_selects_moves_and_sets_group_rates(self):
        player = Mock()
        enemy = Mock()
        player.group = "player-group"
        enemy.group = "enemy-group"
        fight = Fight(player, enemy)

        fight.preparing()

        player.select_fight_moves.assert_called_once_with()
        enemy.select_fight_moves.assert_called_once_with()
        player.set_group_rate.assert_called_once_with("enemy-group")
        enemy.set_group_rate.assert_called_once_with("player-group")

    def test_fight_runs_turns_until_a_turn_returns_false(self, monkeypatch, capsys):
        player = Mock()
        enemy = Mock()
        turn_instance = Mock()
        turn_instance.start.side_effect = [True, False]
        turn_class = Mock(return_value=turn_instance)
        monkeypatch.setattr("src.fighting.Fight.Turn", turn_class)
        fight = Fight(player, enemy)

        fight.fight()

        turn_class.assert_called_once_with(player, enemy)
        assert turn_instance.start.call_count == 2
        assert capsys.readouterr().out.count("----------------------------------------") == 2

    def test_reset_creatures_resets_both_group_rates(self):
        player = Mock()
        enemy = Mock()
        fight = Fight(player, enemy)

        fight.reset_creatures()

        player.reset_group_rate.assert_called_once_with()
        enemy.reset_group_rate.assert_called_once_with()

    def test_set_fight_result_is_loss_when_both_creatures_are_defeated(self, capsys):
        player = Mock(current_hp=0)
        enemy = Mock(current_hp=0)
        fight = Fight(player, enemy)

        fight.set_fight_result()

        assert fight.is_win is False
        player.increase_exp.assert_not_called()
        assert "both of player and enemy die!" in capsys.readouterr().out

    def test_set_fight_result_awards_experience_when_player_wins(self, capsys):
        player = Mock(current_hp=10)
        enemy = Mock(current_hp=0, rank=3)
        fight = Fight(player, enemy)

        fight.set_fight_result()

        assert fight.is_win is True
        player.increase_exp.assert_called_once_with(30)
        assert "you win!" in capsys.readouterr().out

    def test_set_fight_result_is_loss_when_player_is_defeated(self, capsys):
        player = Mock(current_hp=0)
        enemy = Mock(current_hp=10)
        fight = Fight(player, enemy)

        fight.set_fight_result()

        assert fight.is_win is False
        player.increase_exp.assert_not_called()
        assert "you lose" in capsys.readouterr().out

    def test_save_saves_player_model(self, monkeypatch):
        player = Mock()
        model_instance = Mock()
        model_class = Mock(return_value=model_instance)
        monkeypatch.setattr("src.fighting.Fight.PlayerModel", model_class)
        fight = Fight(player, Mock())

        fight.save()

        model_class.assert_called_once_with(player)
        model_instance.save.assert_called_once_with()

    def test_start_runs_fight_lifecycle_and_returns_result(self, monkeypatch, capsys):
        player = Mock()
        enemy = Mock()
        fight = Fight(player, enemy)
        events = []
        monkeypatch.setattr(fight, "preparing", lambda: events.append("preparing"))
        monkeypatch.setattr(fight, "fight", lambda: events.append("fight"))
        monkeypatch.setattr(fight, "reset_creatures", lambda: events.append("reset"))
        monkeypatch.setattr(fight, "set_fight_result", lambda: (events.append("result"), setattr(fight, "is_win", True)))
        monkeypatch.setattr(fight, "save", lambda: events.append("save"))

        result = fight.start()

        assert events == ["preparing", "fight", "reset", "result", "save"]
        assert result is True
        assert "fight start!" in capsys.readouterr().out
