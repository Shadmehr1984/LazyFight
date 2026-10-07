query = """
USE LazyFight;
GO

CREATE TABLE player(
id INT PRIMARY KEY IDENTITY(1, 1),
name VARCHAR(8) NOT NULL UNIQUE,
rank INT NOT NULL DEFAULT 1,
max_hp INT NOT NULL DEFAULT 100,
exp INT NOT NULL DEFAULT 0,
player_group VARCHAR(7) NOT NULL CHECK (player_group IN('rock', 'paper', 'scissor')),
base_defense INT NOT NULL DEFAULT 10,
);

CREATE TABLE move(
id INT PRIMARY KEY NOT NULL IDENTITY(1, 1),
move_type VARCHAR(6) NOT NULL CHECK (move_type IN('attack', 'defend', 'heal', 'nerf', 'buff')),
rank INT NOT NULL DEFAULT 1,
value INT NOT NULL,
accurate FLOAT(2) NOT NULL,
move_target VARCHAR(6),
CHECK ((move_type IN('nerf', 'buff') AND move_target IN('attack', 'heal', 'defend')) OR (move_type IN('attack', 'heal', 'defend') AND move_target IS NULL))
);

CREATE TABLE player_move(
player_id INT NOT NULL,
FOREIGN KEY(player_id) REFERENCES [dbo].[player](id) ON DELETE CASCADE,
move_id INT NOT NULL,
FOREIGN KEY(move_id) REFERENCES [dbo].[move](id) ON DELETE CASCADE,
PRIMARY KEY(player_id, move_id),
);

CREATE TABLE player_inventory(
player_id INT NOT NULL,
FOREIGN KEY(player_id) REFERENCES [dbo].[player](id) ON DELETE CASCADE,
item_name VARCHAR(11) NOT NULL,
PRIMARY KEY(player_id, item_name),
item_count INT NOT NULL CHECK (item_count > 0)
);
"""