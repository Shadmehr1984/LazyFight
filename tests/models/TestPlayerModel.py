from unittest.mock import patch

import pytest

from src.creatures.Group import Group
from src.creatures.Player import Player
from src.models.InventoryModel import InventoryModel
from src.models.MoveModel import MoveModel
from src.models.PlayerModel import PlayerModel


class TestPlayerModel:
    def test_build_update_query_returns_empty_string_when_no_attributes_changed(self):
        player = Player("Raven", 1, Group.rock, 100)
        player.player_id = 12
        model = PlayerModel(player)

        assert model._PlayerModel__build_update_query({}) == ""

    def test_build_update_query_includes_changed_attributes_and_player_id(self):
        player = Player("Raven", 1, Group.rock, 100)
        player.player_id = 12
        model = PlayerModel(player)

        query = model._PlayerModel__build_update_query(
            {"rank": 2, "exp": 25}
        )

        assert query == (
            "UPDATE [dbo].[player]\n"
            "SET \n"
            "rank = 2, exp = 25\n"
            "WHERE id = 12;"
        )

    def test_get_new_attrs_uses_current_player_values(self):
        player = Player("Raven", 2, Group.paper, 200)
        player.exp = 35
        player.base_defense = 20
        model = PlayerModel(player)

        assert model._PlayerModel__get_new_attrs() == {
            "rank": 2,
            "max_hp": 200,
            "exp": 35,
            "player_group": "paper",
            "base_defense": 20,
        }

    @patch("src.models.PlayerModel.Connector")
    def test_insert_new_player_sets_player_id_from_database_result(self, connector):
        player = Player("Raven", 1, Group.rock, 100)
        model = PlayerModel(player)
        connector.result.return_value = [(42,)]

        model._PlayerModel__insert_new_player()

        assert player.player_id == 42
        insert_query = connector.execute.call_args_list[0].args[0]
        assert "INSERT INTO [dbo].[player]" in insert_query
        assert "('Raven', 1, 100, 0, 'rock', 10)" in insert_query
        connector.execute.assert_any_call(
            "SELECT IDENT_CURRENT('player') AS last_id;"
        )

    @patch("src.models.PlayerModel.MoveModel.load_all_players_moves")
    @patch("src.models.PlayerModel.InventoryModel.load_all_players_inventory")
    @patch("src.models.PlayerModel.Connector")
    def test_load_all_players_builds_players_with_related_data(
        self, connector, load_inventories, load_moves
    ):
        connector.result.return_value = [
            (7, "Raven", 2, 200, 35, "paper", 20),
            (8, "Falcon", 1, 100, 0, "rock", 10),
        ]
        inventories = {7: object(), 8: object()}
        moves = {7: ["move-a"], 8: ["move-b"]}
        load_inventories.return_value = inventories
        load_moves.return_value = moves

        players = PlayerModel.load_all_players()

        assert [player.name for player in players] == ["Raven", "Falcon"]
        assert [player.group for player in players] == [Group.paper, Group.rock]
        assert [player.player_id for player in players] == [7, 8]
        assert players[0].rank == 2
        assert players[0].max_hp == 200
        assert players[0].exp == 35
        assert players[0].base_defense == 20
        assert players[0].inventory is inventories[7]
        assert players[0].moves == ["move-a"]
        load_inventories.assert_called_once_with([7, 8])
        load_moves.assert_called_once_with([7, 8])

    @patch("src.models.PlayerModel.MoveModel.load_all_players_moves")
    @patch("src.models.PlayerModel.InventoryModel.load_all_players_inventory")
    @patch("src.models.PlayerModel.Connector")
    def test_load_all_players_raises_for_unknown_group(
        self, connector, load_inventories, load_moves
    ):
        connector.result.return_value = [
            (7, "Raven", 1, 100, 0, "unknown", 10)
        ]
        load_inventories.return_value = {7: object()}
        load_moves.return_value = {7: []}

        with pytest.raises(ValueError, match="should be customize"):
            PlayerModel.load_all_players()
