DROP TABLE IF EXISTS player;
CREATE TABLE player (
	id_player SERIAL PRIMARY KEY,
	username VARCHAR(32) UNIQUE NOT NULL,
	password VARCHAR(128) NOT NULL,
	name VARCHAR(128) NOT NULL,
	date_created TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

DROP TABLE IF EXISTS game;
CREATE TABLE game (
	id_game SERIAL PRIMARY KEY,
	public_id UUID NOT NULL UNIQUE,
	number_players INTEGER,
	date_created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
	date_started TIMESTAMP WITH TIME ZONE,
	date_finished TIMESTAMP WITH TIME ZONE
);

DROP TABLE IF EXISTS turn;
CREATE TABLE turn (
	id_turn SERIAL PRIMARY KEY,
	id_game INTEGER REFERENCES game(id_game) NOT NULL,
	id_player INTEGER REFERENCES player (id_player) NOT NULL,
	x SMALLINT[3] NOT NULL,
	y SMALLINT[3] NOT NULL,
	value SMALLINT[3] NOT NULL,
	score INTEGER NOT NULL,
	date_created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
	UNIQUE (id_game, x, y)
);

DROP TABLE IF EXISTS game_player;
CREATE TABLE game_player (
	id_game_player SERIAL PRIMARY KEY,
	id_game INTEGER REFERENCES game(id_game) NOT NULL,
	id_player INTEGER REFERENCES player(id_player),
	is_game_creator BOOLEAN,
	is_turn BOOLEAN NOT NULL DEFAULT FALSE,
	hand INTEGER[3] NOT NULL DEFAULT '{}',
	points INTEGER NOT NULL DEFAULT 0,
	date_created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
	UNIQUE (id_game, id_player)
);
CREATE UNIQUE INDEX ON game_player (id_game, is_game_creator) WHERE is_game_creator = TRUE;
CREATE INDEX game_player_date_created_idx ON game_player (date_created);
