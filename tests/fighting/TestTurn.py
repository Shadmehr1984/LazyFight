import pytest
from unittest.mock import Mock

from src.fighting.Turn import Turn
from src.moves.Attack import Attack
from src.moves.Buff import Buff
from src.moves.Defend import Defend
from src.moves.Heal import Heal
from src.moves.Nerf import Nerf
from src.moves.MoveTarget import MoveTarget


class TestTurn:
    def test_preparing_selects_turn_moves_for_both_creatures(self):
        player = Mock()
        enemy = Mock()
        turn = Turn(player, enemy)

        turn.preparing()

        player.select_turn_moves.assert_called_once_with()
        enemy.select_turn_moves.assert_called_once_with()

    def test_trigger_takes_and_records_each_creature_turn_move(self):
        player_moves = [Mock() for _ in range(3)]
        enemy_moves = [Mock() for _ in range(3)]
        player = Mock(turn_moves=player_moves)
        enemy = Mock(turn_moves=enemy_moves)
        turn = Turn(player, enemy)

        turn.trigger()

        for move in player_moves + enemy_moves:
            move.move_take.assert_called_once_with()
        for move in player_moves:
            move.is_effected.assert_called_once_with(player)
        for move in enemy_moves:
            move.is_effected.assert_called_once_with(enemy)

    def test_execute_moves_effect_runs_nerf_before_attack_and_targets_opponent(self):
        player = Mock()
        enemy = Mock()
        turn = Turn(player, enemy)
        calls = []
        player_attack = Attack(1, 10, 100, {})
        enemy_nerf = Nerf(1, 0.2, 100, Attack, {})
        player_attack.effect = lambda target: calls.append(("attack", target))
        enemy_nerf.effect = lambda target: calls.append(("nerf", target))

        turn.execute_moves_effect(player_attack, enemy_nerf)

        assert calls == [("nerf", player), ("attack", enemy)]

    def test_execute_moves_effect_targets_owner_for_self_targeted_moves(self):
        player = Mock()
        enemy = Mock()
        turn = Turn(player, enemy)
        calls = []
        player_defend = Defend(1, 10, 100, {})
        enemy_heal = Heal(1, 10, 100, {})
        player_defend.effect = lambda target: calls.append(("defend", target))
        enemy_heal.effect = lambda target: calls.append(("heal", target))

        turn.execute_moves_effect(player_defend, enemy_heal)

        assert calls == [("defend", player), ("heal", enemy)]
        assert player_defend.move_target == MoveTarget.myself
        assert enemy_heal.move_target == MoveTarget.myself

    def test_execute_moves_effect_handles_missing_player_move(self):
        player = Mock()
        enemy = Mock()
        turn = Turn(player, enemy)
        calls = []
        enemy_attack = Attack(1, 10, 100, {})
        enemy_attack.effect = lambda target: calls.append(target)

        turn.execute_moves_effect(None, enemy_attack)

        assert calls == [player]

    def test_execute_moves_effect_handles_both_moves_missing(self):
        turn = Turn(Mock(), Mock())

        turn.execute_moves_effect(None, None)

    def test_reset_creatures_clears_turn_state_and_resets_move_rates(self):
        player = Mock()
        enemy = Mock()
        turn = Turn(player, enemy)

        turn.reset_creatures()

        for creature in (player, enemy):
            creature.clear_turn_moves.assert_called_once_with()
            creature.clear_effected_moves.assert_called_once_with()
            creature.reset_moves_rate.assert_called_once_with()

    def test_start_returns_false_when_either_creature_is_defeated(self, monkeypatch, capsys):
        player = Mock(current_hp=0, effected_moves=[None, None, None], turn_moves=[])
        enemy = Mock(current_hp=100, effected_moves=[None, None, None], turn_moves=[])
        turn = Turn(player, enemy)
        monkeypatch.setattr("src.fighting.Turn.sleep", lambda _seconds: None)
        monkeypatch.setattr(turn, "preparing", lambda: None)
        monkeypatch.setattr(turn, "trigger", lambda: None)
        monkeypatch.setattr(turn, "execute_moves_effect", lambda _player_move, _enemy_move: None)
        monkeypatch.setattr(turn, "reset_creatures", lambda: None)

        result = turn.start()

        assert result is False
        capsys.readouterr()

    def test_start_returns_true_when_both_creatures_remain_alive(self, monkeypatch, capsys):
        player = Mock(current_hp=100, effected_moves=[None, None, None], turn_moves=[])
        enemy = Mock(current_hp=100, effected_moves=[None, None, None], turn_moves=[])
        turn = Turn(player, enemy)
        monkeypatch.setattr("src.fighting.Turn.sleep", lambda _seconds: None)
        monkeypatch.setattr(turn, "preparing", lambda: None)
        monkeypatch.setattr(turn, "trigger", lambda: None)
        monkeypatch.setattr(turn, "execute_moves_effect", lambda _player_move, _enemy_move: None)
        reset = Mock()
        monkeypatch.setattr(turn, "reset_creatures", reset)

        result = turn.start()

        assert result is True
        reset.assert_called_once_with()
        capsys.readouterr()
