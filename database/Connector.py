import mssql_python
from mssql_python import Cursor
from dotenv import load_dotenv
from os import getenv

class Connector:
    load_dotenv()
    
    __connection = None
    __cursor: Cursor = None
    
    @staticmethod
    def __connect() -> None:
        if (Connector.__connection is None):
            connection_string = getenv("SQL_SERVER_CONNECTION_STRING")
            Connector.__connection = mssql_python.connect(connection_string)
            Connector.__cursor = Connector.__connection.cursor()
    
    @staticmethod
    def execute(query: str, *parameters, commit: bool = False, transaction: bool = False):
        Connector.__connect()
        if (transaction):
            query = Connector.__transact_query(query)
        Connector.__cursor.execute(query, parameters)
        if commit: Connector.__cursor.execute('COMMIT;')
    
    @staticmethod
    def __transact_query(query: str):
        transact_query = ""
        transact_query += "BEGIN TRY\n"
        transact_query += "BEGIN TRANSACTION;\n"
        transact_query += query
        transact_query += "COMMIT TRANSACTION\n"
        transact_query += "\nEND TRY\n"
        transact_query += "BEGIN CATCH\n"
        transact_query += "ROLLBACK TRANSACTION;\n"
        transact_query += "END CATCH;"
        
        return transact_query
    
    @staticmethod
    def result():
        try:
            return Connector.__cursor.fetchall()
        except(mssql_python.exceptions.ProgrammingError):
            return
    
    @staticmethod
    def close():
        Connector.__connection = Connector.__connection.close()