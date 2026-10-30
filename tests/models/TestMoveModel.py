from unittest.mock import patch

import pytest

from src.creatures.Group import Group
from src.creatures.Player import Player
from src.models.MoveModel import MoveModel
from src.models.exceptions.PlayerNotExistsException import PlayerNotExistsException
from src.moves.Attack import Attack
from src.moves.Buff import Buff
from src.moves.Defend import Defend
from src.moves.Heal import Heal
from src.moves.Nerf import Nerf


class TestMoveModel:
    def test_build_update_query_returns_empty_string_when_no_moves_changed(self):
        model = MoveModel(Player("Raven", 1, Group.rock, 100))

        assert model._MoveModel__build_update_query([]) == ""

    def test_build_update_query_updates_move_ranks(self):
        model = MoveModel(Player("Raven", 1, Group.rock, 100))

        query = model._MoveModel__build_update_query([(4, "attack", 3, None), (8, "heal", 2, None)])

        assert query == (
            "UPDATE [dbo].[move]\n"
            "SET rank = CASE id\n"
            "  WHEN 4 THEN 3\n"
            "  WHEN 8 THEN 2\n"
            "END\n"
            "WHERE id IN (4,8);"
        )

    def test_build_insert_query_includes_move_and_player_move_rows(self):
        player = Player("Raven", 1, Group.rock, 100)
        player.player_id = 7
        model = MoveModel(player)

        query = model._MoveModel__build_insert_query([
            (21, "attack", 1, None),
            (22, "buff", 2, "heal"),
        ])

        assert "SET IDENTITY_INSERT [dbo].[move] ON;" in query
        assert "(21, 'attack', 1, NULL)" in query
        assert "(22, 'buff', 2, 'heal')" in query
        assert "INSERT INTO [dbo].[player_move](player_id, move_id)" in query
        assert "(7, 21)" in query
        assert "(7, 22)" in query

    def test_build_delete_query_returns_empty_string_or_deletes_ids(self):
        model = MoveModel(Player("Raven", 1, Group.rock, 100))

        assert model._MoveModel__build_delete_query([]) == ""
        assert model._MoveModel__build_delete_query([
            (3, "attack", 1, None),
            (9, "heal", 2, None),
        ]) == "DELETE FROM [dbo].[move]\nWHERE id IN(3,9);"

    @pytest.mark.parametrize(
        ("raw_move", "expected_type"),
        [
            ((1, "attack", 1, None), Attack),
            ((2, "defend", 1, None), Defend),
            ((3, "heal", 1, None), Heal),
            ((4, "buff", 1, "attack"), Buff),
            ((5, "nerf", 1, "defend"), Nerf),
        ],
    )
    def test_convert_raw_move_creates_correct_move_type_and_preserves_id(
        self, raw_move, expected_type
    ):
        move = MoveModel._MoveModel__conv_raw_move_2_move_obj(raw_move)

        assert isinstance(move, expected_type)
        assert move.move_id == raw_move[0]

    @patch("src.models.MoveModel.Connector")
    @patch("src.models.MoveModel.MoveModel._MoveModel__exists")
    @patch("src.models.MoveModel.MoveModel._MoveModel__get_player_moves")
    def test_load_player_moves_converts_database_rows(
        self, get_player_moves, exists, connector
    ):
        get_player_moves.return_value = [
            (11, "attack", 1, None),
            (12, "buff", 1, "heal"),
        ]

        moves = MoveModel.load_player_moves(7)

        exists.assert_called_once_with(7)
        get_player_moves.assert_called_once_with(7)
        assert isinstance(moves[0], Attack)
        assert isinstance(moves[1], Buff)
        assert [move.move_id for move in moves] == [11, 12]

    @patch("src.models.MoveModel.Connector")
    def test_exists_raises_for_missing_player(self, connector):
        connector.result.return_value = [(0,)]

        with pytest.raises(PlayerNotExistsException):
            MoveModel._MoveModel__exists(404)
