# LazyFight

LazyFight is a work-in-progress, text-based dungeon and turn-based combat game written in Python. It includes players and enemies, combat moves, inventory and chests, dungeon generation, menus, tests, and SQL Server persistence.

## Status

The project is under development. `main.py` is the intended entry point, but it is currently excluded by `.gitignore` and is not tracked in this repository. A clean checkout therefore cannot yet launch the game through `main.py`.

## Structure

- `src/creatures/` — players, enemies, and creature groups
- `src/fighting/` — fights, turns, and dungeons
- `src/moves/` — attack, defend, heal, buff, and nerf moves
- `src/things/` — items and inventory
- `src/chests/` — chest logic
- `src/generators/` — dungeon, enemy, move, item, and chest generation
- `src/menus/` — text-based menus
- `src/models/` — data models and persistence
- `database/` — SQL Server connector and migration script
- `tests/` — pytest tests

## Requirements

Python 3.10+ is a reasonable starting point. The tracked code imports `mssql-python` and `python-dotenv`; tests use `pytest`. No `requirements.txt` or dependency lockfile is present yet.

Install the identified packages:

```bash
python -m pip install mssql-python python-dotenv pytest
```

Configure SQL Server and set `SQL_SERVER_CONNECTION_STRING` in a local `.env` file. Never commit credentials. Review `database/migrate.py` before running it against your database.

## Tests

Run from the repository root:

```bash
python -m pytest
```

The game startup flow and database initialization are not yet documented as a verified end-to-end process.

## License

No license is currently specified in the repository.
