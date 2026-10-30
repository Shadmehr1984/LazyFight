from unittest.mock import Mock, patch

import mssql_python

from database.Connector import Connector


class TestConnector:
    def setup_method(self):
        Connector._Connector__connection = None
        Connector._Connector__cursor = None

    def test_execute_connects_and_passes_query_parameters(self):
        connection = Mock()
        cursor = connection.cursor.return_value
        with patch("database.Connector.getenv", return_value="connection-string"), \
             patch("database.Connector.mssql_python.connect", return_value=connection):
            Connector.execute("SELECT ?", 7)
        connection.cursor.assert_called_once_with()
        cursor.execute.assert_called_once_with("SELECT ?", (7,))

    def test_execute_wraps_transaction_query_and_commits_when_requested(self):
        connection = Mock()
        cursor = connection.cursor.return_value
        with patch("database.Connector.getenv", return_value="connection-string"), \
             patch("database.Connector.mssql_python.connect", return_value=connection):
            Connector.execute("UPDATE thing SET value = 1;", commit=True, transaction=True)
        query = cursor.execute.call_args_list[0].args[0]
        assert query.startswith("BEGIN TRY\nBEGIN TRANSACTION;")
        assert "ROLLBACK TRANSACTION;" in query
        assert cursor.execute.call_args_list[1].args[0] == "COMMIT;"

    def test_result_returns_rows(self):
        cursor = Mock()
        cursor.fetchall.return_value = [(1,)]
        Connector._Connector__cursor = cursor
        assert Connector.result() == [(1,)]

    def test_result_returns_none_when_fetchall_has_no_result_set(self):
        cursor = Mock()
        cursor.fetchall.side_effect = mssql_python.exceptions.ProgrammingError("no result")
        Connector._Connector__cursor = cursor
        assert Connector.result() is None
