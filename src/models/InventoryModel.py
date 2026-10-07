from database.Connector import Connector
from src.things.Inventory import Inventory
from src.things.Item import Item
from src.models.exceptions.PlayerNotExistsException import PlayerNotExistsException

class InventoryModel:
    def __init__(self, player_id: int, inventory: Inventory) -> None:
        self.player_id = player_id
        self.inventory = inventory
    
    @staticmethod
    def load(player_id: int) -> Inventory:
        exists = InventoryModel.__exists(player_id)
        
        if (not exists):
            raise PlayerNotExistsException()
        
        query = f"SELECT item_name, item_count FROM player_inventory WHERE player_id = {player_id}"
        
        Connector.execute(query)
        items = Connector.result()
        
        inventory = Inventory()
        
        for item in items:
            inventory.add_item(Item(item[0], item[1]))
        
        return inventory
    
    def save(self):
        exists = self.__exists(self.player_id)
        
        if (not exists):
            raise PlayerNotExistsException()
        
        #old_inventory = [(item_name1, item_count1), ...]
        old_inventory = self.__get_old_inventory()
        
        #new_inventory = [(item_name1, item_count1), ...]
        new_inventory = self.__get_new_inventory()
        
        update_items = []
        delete_items = []
        insert_items = []
        
        update_items = []

        old_dict = {item[0]: item for item in old_inventory}

        remaining_new = []

        for new_item in new_inventory:
            key = new_item[0]
            if key in old_dict:
                old_item = old_dict[key]
                if new_item[1] != old_item[1]:
                    update_items.append(new_item)
                del old_dict[key]
            else:
                remaining_new.append(new_item)

        remaining_old = list(old_dict.values())

        new_inventory[:] = remaining_new
        old_inventory[:] = remaining_old
        
        for new_inventory_item in new_inventory:
            insert_items.append(new_inventory_item)
        
        #if a item is still in old inventory that means item must be deleted
        for old_inventory_item in old_inventory:
            delete_items.append(old_inventory_item)
        
        query = ""
        query += self.__build_update_query(update_items)
        query += "\n"
        query += self.__build_insert_query(insert_items)
        query += "\n"
        query += self.__build_delete_query(delete_items)
        
        Connector.execute(query, commit=True)
    
    @staticmethod
    def __exists(player_id: int) -> bool:
        Connector.execute(f"SELECT COUNT(*) FROM dbo.player WHERE id = {player_id}")
        
        #result is a list of tuples
        result = Connector.result()[0][0]
        
        match result:
            case 1:
                return True
            case 0:
                return False
    
    def __get_old_inventory(self):
        old_inventory = None
        
        Connector.execute(f"SELECT item_name, item_count FROM dbo.player_inventory WHERE player_id = {self.player_id}")
        old_inventory = Connector.result()
        
        return old_inventory
    
    def __get_new_inventory(self):
        new_inventory = []
        
        for item_name in self.inventory.items:
            item_count = self.inventory.items[item_name].count
            item = (item_name, item_count)
            new_inventory.append(item)
        
        return new_inventory

    def __build_update_query(self, update_items) -> str:
        if (len(update_items) == 0):
            return ""

        set_clause_statement = ""
        
        where_clause_statement = ""
        
        for item in update_items:
            set_clause_statement += f"  WHEN \'{item[0]}\' THEN {item[1]}\n"
            where_clause_statement += f"\'{item[0]}\',"
        
        #delete last ','
        where_clause_statement = where_clause_statement[:-1]
        
        where_clause_statement = f"WHERE item_name IN ({where_clause_statement})"
        
        query = "UPDATE [dbo].[player_inventory]\nSET item_count = CASE item_name\n"
        query += set_clause_statement
        query += "END\n"
        query += where_clause_statement
        query += ";"
        
        return query
    
    def __build_insert_query(self, insert_items) -> str:
        if (len(insert_items) == 0):
            return ""
        
        values_clause_statement = ""
        
        for item in insert_items:
            values_clause_statement += f"({self.player_id}, \'{item[0]}\', {item[1]}),\n"
        
        #delete last \n and last ','
        values_clause_statement = values_clause_statement[:-2]
        
        query = "INSERT INTO [dbo].[player_inventory](player_id, item_name, item_count)\n"
        query += "VALUES"
        query += values_clause_statement
        query += ";"
        
        return query
    
    def __build_delete_query(self, delete_items) -> str:
        if (len(delete_items) == 0):
            return ""
        
        where_clause_statement = ""
        
        for item in delete_items:
            where_clause_statement += f"\'{item[0]}\',"
        
        #delete last ','
        where_clause_statement = where_clause_statement[:-1]
        
        where_clause_statement = "(" + where_clause_statement + ")"
        
        query = "DELETE FROM [dbo].[player_inventory]\n"
        query += "WHERE item_name IN"
        query += where_clause_statement
        query += ";"
        
        return query