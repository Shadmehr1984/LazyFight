import pytest

from src.creatures.Group import Group
from src.creatures.Player import Player
from src.creatures.exceptions.NotEnoughMovesException import NotEnoughMoveException


class DummyMove:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class TestPlayer:
    def test_initial_player(self):
        player = Player("Raven", 1, Group.rock, 100)

        assert player.player_id is None
        assert player.exp == 0
        assert player.rank == 1
        assert player.max_hp == 100
        assert player.name == "Raven"

    def test_rank_up_updates_rank_hp_and_base_defense(self):
        player = Player("Raven", 1, Group.rock, 100)
        player.exp = 100

        player.rank_up()

        assert player.rank == 2
        assert player.exp == 0
        assert player.max_hp == 200
        assert player.base_defense == 20

    def test_increase_exp_without_reaching_threshold(self):
        player = Player("Raven", 1, Group.rock, 100)

        player.increase_exp(50)

        assert player.exp == 50
        assert player.rank == 1

    def test_increase_exp_triggers_rank_up(self):
        player = Player("Raven", 1, Group.rock, 100)

        player.increase_exp(100)

        assert player.rank == 2
        assert player.exp == 0
        assert player.max_hp == 200
        assert player.base_defense == 20

    def test_increase_exp_can_trigger_multiple_rank_ups(self):
        player = Player("Raven", 1, Group.rock, 100)

        player.increase_exp(300)

        assert player.rank == 3
        assert player.exp == 0
        assert player.max_hp == 300
        assert player.base_defense == 30

    def test_select_fight_moves_raises_when_fewer_than_three_moves(self):
        player = Player("Raven", 1, Group.rock, 100)
        player.moves = [DummyMove("one"), DummyMove("two")]

        with pytest.raises(NotEnoughMoveException):
            player.select_fight_moves()

    def test_select_fight_moves_copies_moves_when_six_or_fewer(self, capsys):
        player = Player("Raven", 1, Group.rock, 100)
        player.moves = [DummyMove(str(index)) for index in range(3)]

        player.select_fight_moves()

        assert player.fight_moves == player.moves
        assert player.fight_moves is not player.moves
        assert "fight moves selected" in capsys.readouterr().out

    def test_select_fight_moves_does_not_share_list_with_moves(self, capsys):
        player = Player("Raven", 1, Group.rock, 100)
        player.moves = [DummyMove(str(index)) for index in range(3)]

        player.select_fight_moves()
        player.fight_moves.append(DummyMove("extra"))

        assert len(player.moves) == 3
        assert len(player.fight_moves) == 4

    def test_select_fight_moves_uses_input_when_more_than_six_moves(self, monkeypatch, capsys):
        player = Player("Raven", 1, Group.rock, 100)
        player.moves = [DummyMove(str(index)) for index in range(7)]
        answers = iter(["0", "1", "2", "3", "4", "5"])
        monkeypatch.setattr("builtins.input", lambda: next(answers))

        player.select_fight_moves()

        assert player.fight_moves == player.moves[:6]
        assert len(player.fight_moves) == 6

    def test_select_turn_moves_raises_when_fewer_than_three_moves(self):
        player = Player("Raven", 1, Group.rock, 100)
        player.moves = [DummyMove("one"), DummyMove("two")]

        with pytest.raises(NotEnoughMoveException):
            player.select_turn_moves()

    def test_select_turn_moves_selects_three_distinct_moves(self, monkeypatch, capsys):
        player = Player("Raven", 1, Group.rock, 100)
        player.moves = [DummyMove(str(index)) for index in range(6)]
        player.select_fight_moves()
        answers = iter(["0", "1", "2"])
        monkeypatch.setattr("builtins.input", lambda: next(answers))

        player.select_turn_moves()

        assert player.turn_moves == player.fight_moves[:3]
        assert len(player.turn_moves) == 3

    def test_str_includes_experience(self):
        player = Player("Raven", 2, Group.paper, 200)
        player.exp = 35

        assert str(player) == "Raven, group:paper, rank:2, hp:200, defense:0, exp:35"

    def test_players_are_equal_when_names_match(self):
        first = Player("Raven", 1, Group.rock, 100)
        second = Player("Raven", 5, Group.paper, 500)

        assert first == second

    def test_players_are_not_equal_when_names_differ(self):
        first = Player("Raven", 1, Group.rock, 100)
        second = Player("Falcon", 1, Group.rock, 100)

        assert first != second
