from unittest.mock import patch

import pytest

from src.creatures.Group import Group
from src.creatures.Player import Player
from src.models.InventoryModel import InventoryModel
from src.models.exceptions.PlayerNotExistsException import PlayerNotExistsException
from src.things.Inventory import Inventory
from src.things.Item import Item


class TestInventoryModel:
    def test_init_keeps_player_id_and_inventory(self):
        player = Player("Raven", 1, Group.rock, 100)
        player.player_id = 9
        player.inventory.add_item(Item("potion", 2))

        model = InventoryModel(player)

        assert model.player_id == 9
        assert model.inventory is player.inventory

    @patch("src.models.InventoryModel.Connector")
    def test_load_all_players_inventory_creates_separate_inventories(self, connector):
        connector.result.return_value = [
            (1, "potion", 2),
            (1, "potion", 3),
            (2, "shield", 1),
        ]

        inventories = InventoryModel.load_all_players_inventory([1, 2, 3])

        assert inventories[1].get() == {"potion": 5}
        assert inventories[2].get() == {"shield": 1}
        assert inventories[3].get() == {}
        assert inventories[1] is not inventories[2]
        connector.execute.assert_called_once_with(
            "SELECT player_id, item_name, item_count FROM player_inventory WHERE player_id IN (1,2,3)"
        )

    @patch("src.models.InventoryModel.Connector")
    def test_load_player_inventory_returns_items(self, connector):
        connector.result.side_effect = [
            [(1,)],
            [("potion", 2), ("ether", 1)],
        ]

        inventory = InventoryModel.load_player_inventory(5)

        assert inventory.get() == {"potion": 2, "ether": 1}
        assert connector.execute.call_count == 2
        assert "WHERE player_id = 5" in connector.execute.call_args_list[1].args[0]

    @patch("src.models.InventoryModel.Connector")
    def test_load_player_inventory_raises_for_missing_player(self, connector):
        connector.result.return_value = [(0,)]

        with pytest.raises(PlayerNotExistsException):
            InventoryModel.load_player_inventory(99)

    @patch("src.models.InventoryModel.Connector")
    def test_save_get_query_builds_update_insert_and_delete_statements(self, connector):
        player = Player("Raven", 1, Group.rock, 100)
        player.player_id = 5
        player.inventory.add_item(Item("potion", 3))
        player.inventory.add_item(Item("ether", 4))
        model = InventoryModel(player)
        connector.result.side_effect = [
            [(1,)],
            [("potion", 2), ("old_item", 1)],
        ]

        query = model.save(get_query=True)

        assert "UPDATE [dbo].[player_inventory]" in query
        assert "WHEN 'potion' THEN 3" in query
        assert "INSERT INTO [dbo].[player_inventory]" in query
        assert "(5, 'ether', 4)" in query
        assert "DELETE FROM [dbo].[player_inventory]" in query
        assert "item_name IN('old_item')" in query

    @patch("src.models.InventoryModel.Connector")
    def test_save_without_changes_returns_empty_query(self, connector):
        player = Player("Raven", 1, Group.rock, 100)
        player.player_id = 5
        player.inventory.add_item(Item("potion", 2))
        model = InventoryModel(player)
        connector.result.side_effect = [
            [(1,)],
            [("potion", 2)],
        ]

        query = model.save(get_query=True)

        assert query.strip() == ""
