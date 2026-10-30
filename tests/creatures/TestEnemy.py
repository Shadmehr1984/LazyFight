import pytest

from src.creatures.Enemy import Enemy
from src.creatures.Group import Group
from src.creatures.exceptions.NotEnoughMovesException import NotEnoughMoveException


class DummyMove:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class TestEnemy:
    def test_initial_enemy(self):
        enemy = Enemy("Goblin", 2, Group.scissor, 150)

        assert enemy.name == "Goblin"
        assert enemy.rank == 2
        assert enemy.group == Group.scissor
        assert enemy.max_hp == 150
        assert enemy.current_hp == 150
        assert enemy.moves == []
        assert enemy.fight_moves == []
        assert enemy.turn_moves == []

    def test_select_fight_moves_raises_when_fewer_than_three_moves(self):
        enemy = Enemy("Goblin", 1, Group.rock, 100)
        enemy.moves = [DummyMove("one"), DummyMove("two")]

        with pytest.raises(NotEnoughMoveException):
            enemy.select_fight_moves()

    def test_select_fight_moves_copies_all_moves_when_six_or_fewer(self, capsys):
        enemy = Enemy("Goblin", 1, Group.rock, 100)
        enemy.moves = [DummyMove(str(index)) for index in range(3)]

        enemy.select_fight_moves()

        assert enemy.fight_moves == enemy.moves
        assert enemy.fight_moves is not enemy.moves
        assert "enemy select his fight moves" in capsys.readouterr().out

    def test_select_fight_moves_selects_six_unique_moves_when_more_than_six(self, monkeypatch, capsys):
        enemy = Enemy("Goblin", 1, Group.rock, 100)
        enemy.moves = [DummyMove(str(index)) for index in range(8)]
        values = iter([0, 1, 2, 3, 4, 5])
        monkeypatch.setattr("src.creatures.Enemy.randint", lambda _start, _end: next(values))

        enemy.select_fight_moves()

        assert enemy.fight_moves == enemy.moves[:6]
        assert len(enemy.fight_moves) == 6
        assert len(set(map(id, enemy.fight_moves))) == 6
        assert "enemy select his fight moves" in capsys.readouterr().out

    def test_select_fight_moves_retries_duplicate_random_selection(self, monkeypatch, capsys):
        enemy = Enemy("Goblin", 1, Group.rock, 100)
        enemy.moves = [DummyMove(str(index)) for index in range(7)]
        values = iter([0, 0, 1, 2, 3, 4, 5])
        monkeypatch.setattr("src.creatures.Enemy.randint", lambda _start, _end: next(values))

        enemy.select_fight_moves()

        assert enemy.fight_moves == enemy.moves[:6]
        assert len(enemy.fight_moves) == 6

    def test_select_turn_moves_raises_when_fewer_than_three_moves(self):
        enemy = Enemy("Goblin", 1, Group.rock, 100)
        enemy.moves = [DummyMove("one"), DummyMove("two")]

        with pytest.raises(NotEnoughMoveException):
            enemy.select_turn_moves()

    def test_select_turn_moves_selects_three_distinct_fight_moves(self, monkeypatch, capsys):
        enemy = Enemy("Goblin", 1, Group.rock, 100)
        enemy.moves = [DummyMove(str(index)) for index in range(6)]
        enemy.fight_moves = enemy.moves.copy()
        values = iter([0, 1, 2])
        monkeypatch.setattr("src.creatures.Enemy.randint", lambda _start, _end: next(values))

        enemy.select_turn_moves()

        assert enemy.turn_moves == enemy.fight_moves[:3]
        assert len(enemy.turn_moves) == 3
        assert "enemy select his turn moves" in capsys.readouterr().out

    def test_select_turn_moves_retries_duplicate_random_selection(self, monkeypatch, capsys):
        enemy = Enemy("Goblin", 1, Group.rock, 100)
        enemy.moves = [DummyMove(str(index)) for index in range(6)]
        enemy.fight_moves = enemy.moves.copy()
        values = iter([0, 0, 1, 2])
        monkeypatch.setattr("src.creatures.Enemy.randint", lambda _start, _end: next(values))

        enemy.select_turn_moves()

        assert enemy.turn_moves == enemy.fight_moves[:3]
        assert len(enemy.turn_moves) == 3
