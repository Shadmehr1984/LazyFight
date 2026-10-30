from src.moves.Move import Move
from src.moves.Attack import Attack
from src.moves.Buff import Buff
from src.moves.Defend import Defend
from src.moves.Heal import Heal
from src.moves.Nerf import Nerf
from src.creatures.Player import Player
from src.models.exceptions.PlayerNotExistsException import PlayerNotExistsException
from database.Connector import Connector
from src.generators.MoveGenerator import MoveGenerator

class MoveModel:
    #this kept last move id in db
    last_id = None
    
    def __init__(self, player: Player) -> None:
        self.player = player
    
    #if get_query is True, nothing run on DB and just return the query
    def save(self, get_query: bool = False):
        MoveModel.__exists(self.player.player_id)
        
        old_moves = self.__get_old_moves()
        
        new_moves = self.__get_new_moves()
        
        update_moves = []
        insert_moves = []
        delete_moves = []
        
        old_moves_dict = {move[0]: move for move in old_moves}
        
        temp_new_moves = []
        temp_old_moves = []
        
        for new_move in new_moves:
            key = new_move[0]
            if key in old_moves_dict:
                old_move = old_moves_dict[key]
                #new_move[2] == rank
                if new_move[2] != old_move[2]:
                    update_moves.append(new_move)
                del old_moves_dict[key]
            else:
                temp_new_moves.append(new_move)
        
        temp_old_moves = list(old_moves_dict.values())

        new_moves[:] = temp_new_moves
        old_moves[:] = temp_old_moves
        
        for new_move in new_moves:
            insert_moves.append(new_move)
        
        #if a move is still in old moves that means item must be deleted
        for old_move in old_moves:
            delete_moves.append(old_move)
        
        query = ""
        query += self.__build_update_query(update_moves)
        query += "\n"
        query += self.__build_insert_query(insert_moves)
        query += "\n"
        query += self.__build_delete_query(delete_moves)
        
        if (get_query):
            return query
        
        Connector.execute(query, commit=True)
    
    def __build_update_query(self, update_moves: list[tuple]) -> str:
        if (len(update_moves) == 0):
            return ""

        set_clause_statement = ""
        
        where_clause_statement = ""
        
        for move in update_moves:
            set_clause_statement += f"  WHEN {move[0]} THEN {move[2]}\n"
            where_clause_statement += f"{move[0]},"
        
        #delete last ','
        where_clause_statement = where_clause_statement[:-1]
        
        where_clause_statement = f"WHERE id IN ({where_clause_statement})"
        
        query = "UPDATE [dbo].[move]\nSET rank = CASE id\n"
        query += set_clause_statement
        query += "END\n"
        query += where_clause_statement
        query += ";"
        
        return query
    
    def __build_insert_query(self, insert_moves: list[tuple]) -> str:
        if (len(insert_moves) == 0):
            return ""
        
        value_clause_statement = ""
        
        for move in insert_moves:
            move_target = "NULL"
            if (move[3] is not None):
                move_target = f"\'{move[3]}\'"
            value_clause_statement += f"({move[0]}, \'{move[1]}\', {move[2]}, {move_target}),\n"
        
        #delete last , and \n
        value_clause_statement = value_clause_statement[:-2]
        
        next_value_clause_statement = ""
        
        for move in insert_moves:
            next_value_clause_statement += f"({self.player.player_id}, {move[0]}),\n"
        
        #delete last , and \n
        next_value_clause_statement = next_value_clause_statement[:-2]
        #before insert should set IDENTITY_INSERT to ON
        query = "SET IDENTITY_INSERT [dbo].[move] ON;\n"
        
        query += "INSERT INTO [dbo].[move](id, move_type, rank, move_target)\n"
        query += "VALUES"
        query += value_clause_statement
        query += ";\n"
        query += "INSERT INTO [dbo].[player_move](player_id, move_id)\n"
        query += "VALUES"
        query += next_value_clause_statement
        query += ";"
        
        return query

    def __build_delete_query(self, delete_moves) -> str:
        if (len(delete_moves) == 0):
            return ""
        
        where_clause_statement = ""
        
        for move in delete_moves:
            where_clause_statement += f"{move[0]},"
        
        #delete last ','
        where_clause_statement = where_clause_statement[:-1]
        
        where_clause_statement = "(" + where_clause_statement + ")"
        
        query = "DELETE FROM [dbo].[move]\n"
        query += "WHERE id IN"
        query += where_clause_statement
        query += ";"
        
        return query

    def __get_old_moves(self):
        query = f"""
        SELECT player_move.move_id, move.move_type, move.rank, move.move_target
        FROM player_move
        LEFT JOIN move
        ON player_move.move_id = move.id
        WHERE player_move.player_id = {self.player.player_id};
        """

        Connector.execute(query)
        
        return Connector.result()

    def __get_new_moves(self):
        new_moves = []
        
        #get last move id from db and store in last_id static attr 
        self.__get_last_id()
        
        for move in self.player.moves:
            if (move.move_id is None):
                self.__set_move_id(move)
            move_id = move.move_id
            
            move_type = None
            if (isinstance(move, Attack)):
                move_type = 'attack'
            elif (isinstance(move, Defend)):
                move_type = 'defend'
            elif (isinstance(move, Heal)):
                move_type = 'heal'
            elif (isinstance(move, Nerf)):
                move_type = 'nerf'
            elif (isinstance(move, Buff)):
                move_type = 'buff'
            else:
                raise ValueError('it should be customize')

            move_rank = move.rank
            
            move_target = None
            
            if (isinstance(move, Nerf) or isinstance(move, Buff)):
                if (move.move_class == Attack):
                    move_target = 'attack'
                elif (move.move_class == Heal):
                    move_target = 'heal'
                elif(move.move_class == Defend):
                    move_target = 'defend'
                else:
                    print(move.move_class)
                    raise ValueError('it should be customize')
            
            new_moves.append(tuple([move_id, move_type, move_rank, move_target]))
        
        return new_moves

    def __set_move_id(self, move: Move):
        MoveModel.last_id += 1
        move.move_id = MoveModel.last_id
    
    @staticmethod
    def __get_last_id():
        query = "SELECT IDENT_CURRENT('move') AS last_id"
        Connector.execute(query)
        #[(last_id)]
        MoveModel.last_id = Connector.result()[0][0]
    
    @staticmethod
    def load_player_moves(player_id: int) -> list[Move]:
        MoveModel.__exists(player_id)
        
        moves = MoveModel.__get_player_moves(player_id)
        
        for move_index in range(0, len(moves)):
            move = moves[move_index]
            
            move_id = move[0]
            
            match move[1]:
                case 'attack':
                    move = MoveGenerator.generate(move[2], 'attack')
                case 'defend':
                    move = MoveGenerator.generate(move[2], 'defend')
                case 'heal':
                    move = MoveGenerator.generate(move[2], 'heal')
                case 'buff':
                    move = MoveGenerator.generate(move[2], 'buff', move[3])
                case 'nerf':
                    move = MoveGenerator.generate(move[2], 'nerf', move[3])
            
            move.move_id = move_id
            
            moves[move_index] = move
        
        return moves
    
    @staticmethod
    def __exists(player_id: int):
        Connector.execute(f"SELECT COUNT(*) FROM dbo.player WHERE id = {player_id}")
        
        #result is a list of tuples
        result = Connector.result()[0][0]
        
        exists = None
        
        match result:
            case 1:
                exists = True
            case 0:
                exists = False
        
        if (not exists):
            raise PlayerNotExistsException()
    
    @staticmethod
    def __get_player_moves(player_id: int):
        query = f"""
        SELECT move.id, move.move_type, move.rank, move.move_target
        FROM player_move
        LEFT JOIN move
        ON move.id = player_move.move_id
        WHERE player_id = {player_id}
        """
        
        Connector.execute(query)
        
        moves = Connector.result()
        
        return moves