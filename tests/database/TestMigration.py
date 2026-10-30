from database import migrate


class TestMigration:
    def test_schema_creates_expected_tables(self):
        for table in ("player", "move", "player_move", "player_inventory"):
            assert f"CREATE TABLE {table}(" in migrate.query

    def test_schema_contains_key_constraints(self):
        assert "name VARCHAR(8) NOT NULL UNIQUE" in migrate.query
        assert "player_group IN('rock', 'paper', 'scissor')" in migrate.query
        assert "item_count INT NOT NULL CHECK (item_count > 0)" in migrate.query
        assert "ON DELETE CASCADE" in migrate.query
