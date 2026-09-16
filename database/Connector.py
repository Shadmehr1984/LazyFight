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
    def execute(query: str, *parameters, commit: bool = False):
        Connector.__connect()
        Connector.__cursor.execute(query, parameters)
        if commit: Connector.__cursor.execute('COMMIT;')
    
    @staticmethod
    def result():
        try:
            return Connector.__cursor.fetchall()
        except(mssql_python.exceptions.ProgrammingError):
            return
    
    @staticmethod
    def close():
        Connector.__connection = Connector.__connection.close()