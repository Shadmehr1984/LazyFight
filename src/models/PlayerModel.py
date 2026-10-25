from src.creatures.Player import Player
from src.creatures.Group import Group
from src.models.InventoryModel import InventoryModel
from src.models.MoveModel import MoveModel
from database.Connector import Connector

class PlayerModel:
    def __init__(self, player: Player) -> None:
        self.player = player
    
    def save(self):
        if (self.player.player_id == None):
            self.__insert_new_player()
        
        old_attrs = self.__get_old_attrs()
        
        new_attrs = self.__get_new_attrs()
        
        update_attrs = {}
        
        for key in old_attrs.keys():
            if old_attrs[key] != new_attrs[key]:
                update_attrs[key] = new_attrs[key]
        
        query = self.__build_update_query(update_attrs)
        
        Connector.execute(query, commit=True)
        
        (InventoryModel(self.player)).save()
        (MoveModel(self.player)).save()
    
    def __build_update_query(self, update_attrs: dict) -> str:
        if (len(update_attrs) == 0):
            return ""
        
        query = "UPDATE [dbo].[player]\n"
        query += "SET \n"
        for key in update_attrs.keys():
            query += f"{key} = {update_attrs[key]}, "
        #delete last , and space
        query = query[:-2]
        query += "\n"
        query += f"WHERE id = {self.player.player_id};"
        
        return query
    
    def __get_new_attrs(self):
        new_attrs = {
            'rank': self.player.rank,
            'max_hp': self.player.max_hp,
            'exp': self.player.exp,
            'player_group': self.player.group.name,
            'base_defense': self.player.base_defense
        }
        
        return new_attrs
    
    def __get_old_attrs(self):
        query = f"""
        SELECT[rank]
            ,[max_hp]
            ,[exp]
            ,[player_group]
            ,[base_defense]
        FROM [LazyFight].[dbo].[player]
        WHERE [id] = {self.player.player_id}
        """
        
        Connector.execute(query)
        
        result = Connector.result()[0]
        
        old_attrs = {
            'rank': result[0],
            'max_hp': result[1],
            'exp': result[2],
            'player_group': result[3],
            'base_defense': result[4]
        }
        
        return old_attrs
    
    def __insert_new_player(self):
        query = ""
        query += "INSERT INTO [dbo].[player](name, rank, max_hp, exp, player_group, base_defense)\n"
        query += "VALUES"
        query += f"(\'{self.player.name}\', {self.player.rank}, {self.player.max_hp}, {self.player.exp}, \'{self.player.group.name}\', {self.player.base_defense})"
        query += ";"
        
        Connector.execute(query, commit=True)
        
        #get player id
        query = "SELECT IDENT_CURRENT('player') AS last_id;"
        
        Connector.execute(query)
        
        #[(last_id)]
        last_id = Connector.result()[0][0]
        
        self.player.player_id = last_id
    
    @staticmethod
    def load_all_players() -> list[Player]:
        query = """
        SELECT TOP 1000 [id]
        ,[name]
        ,[rank]
        ,[max_hp]
        ,[exp]
        ,[player_group]
        ,[base_defense]
        FROM [LazyFight].[dbo].[player];
        """
        
        Connector.execute(query)
        
        players = Connector.result()
        
        for player_index in range(0, len(players)):
            player = players[player_index]
            
            player_id = player[0]
            
            player_name = player[1]
            
            player_rank = player[2]
            
            player_max_hp = player[3]
            
            player_exp = player[4]
            
            player_group = None
            match player[5]:
                case 'rock':
                    player_group = Group.rock
                case 'paper':
                    player_group = Group.paper
                case 'scissor':
                    player_group = Group.scissor
                case default:
                    raise ValueError('should be customize')
            
            player_base_defense = player[6]
            
            player = Player(player_name, player_rank, player_group, player_max_hp)
            player.player_id = player_id
            player.base_defense = player_base_defense
            player.exp = player_exp
            
            player.inventory = InventoryModel.load_player_inventory(player_id)
            player.moves = MoveModel.load_player_moves(player_id)
            
            players[player_index] = player
        
        return players