# LazyFight

LazyFight is a work-in-progress, text-based dungeon crawler with turn-based combat, written in Python. Players can fight enemies, explore dungeons, collect items, manage an inventory, and improve their moves.

Player, move, and inventory data are persisted in Microsoft SQL Server.

## Project Status

The project is under active development. The application now has a tracked entry point in `main.py`; it is no longer excluded by `.gitignore`.

The current startup flow is:

1. `main.py` loads saved players through `PlayerModel.load_all_players()`.
2. It passes those players to `MainMenu`.
3. `MainMenu.open()` starts the text-based main menu.

The game and its database setup are still evolving. In particular, the current player-loading path expects saved player records, so first-run handling for an empty player table still needs work.

## Features and Systems

- Player and enemy creatures, with ranks, health, defense, and groups.
- Turn-based combat with Attack, Defend, Heal, Buff, and Nerf moves.
- Move selection and move rank upgrades.
- Dungeon, enemy, move, item, and chest generation.
- Player inventory and chest rewards.
- SQL Server persistence for players, moves, and inventory.
- Text-based menus for player creation, player selection, dungeons, moves, and inventory.

## Project Structure

- `main.py` — application entry point.
- `src/creatures/` — base creatures, players, enemies, and creature groups.
- `src/fighting/` — fights, turns, and dungeons.
- `src/moves/` — combat move classes and move targets.
- `src/things/` — items and inventory.
- `src/chests/` — chest logic and chest-related exceptions.
- `src/generators/` — generators for dungeons, enemies, moves, items, and chests.
- `src/menus/` — text-based application menus.
- `src/models/` — persistence models for players, moves, and inventory.
- `database/` — SQL Server connector and database schema draft.
- `tests/` — automated tests.

## Requirements

- Python 3.10 or later.
- A Microsoft SQL Server instance.
- Python packages:
  - `mssql-python`
  - `python-dotenv`
  - `pytest` (for running tests)

Install the packages from the repository root:

```bash
python -m pip install mssql-python python-dotenv pytest
```

## Database Configuration

The application reads its SQL Server connection string from the `SQL_SERVER_CONNECTION_STRING` environment variable. For local development, put it in a `.env` file in the repository root:

```dotenv
SQL_SERVER_CONNECTION_STRING="your SQL Server connection string"
```

Do not commit your real connection string or other credentials.

The application expects a database named `LazyFight` with the tables defined by the project schema. The current `database/migrate.py` file stores SQL in a Python variable named `query`; running it as a Python script does not execute that SQL. Review the schema, create the database, and apply the SQL using your SQL Server administration tool before starting the application.

## Run the Game

From the repository root, run:

```bash
python main.py
```

The entry point loads the saved players from SQL Server and opens the main menu. A working database connection and the expected schema are required.

## Run Tests

From the repository root:

```bash
python -m pytest
```

## License

No license is currently specified in the repository.
