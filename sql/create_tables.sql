CREATE EXTENSION IF NOT EXISTS postgis;

DROP TABLE IF EXISTS roads;

CREATE TABLE roads (
	id SERIAL PRIMARY KEY,
	osm_id BIGINT,
	code INTEGER,
	fclass TEXT,
	name TEXT,
	ref TEXT,
	oneway TEXT,
	maxspeed INTEGER,
	geom GEOMETRY(LineString, 4326)
);
