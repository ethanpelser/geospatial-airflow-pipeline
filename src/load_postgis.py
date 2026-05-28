from pathlib import Path

import pyogrio
from sqlalchemy import create_engine, text

DB_URL = "postgresql://airflow:airflow@postgres:5432/geospatial"
SHAPEFILE_PATH = Path("data/raw/osm/gis_osm_roads_free_1.shp")
BATCH_SIZE = 2000
MAX_ROWS = 10000


def load_roads_to_postgis():
	"""Load OpenStreetMap roads shapefile into PostGIS in chunks and also clean it.
	"""
	print("connecting to PostGIS database")
	engine = create_engine(DB_URL)
	
	print("Clearing existing roads table")

	with engine.begin() as conn:
		conn.execute(text("TRUNCATE TABLE roads;"))

	offset = 0
	total_inserted = 0

	while total_inserted < MAX_ROWS:
		print(f"Reading rows {offset} to {offset + BATCH_SIZE}")

		roads = pyogrio.read_dataframe(
			SHAPEFILE_PATH,
			skip_features = offset,
			max_features = BATCH_SIZE
		)

		if roads.empty:
			break

		roads = roads[
			[
				
                		"osm_id",
                		"code",
                		"fclass",
                		"name",
                		"ref",
                		"oneway",
                		"maxspeed",
                		"geometry",
			]
        	]

		roads = roads.dropna(subset = ["geometry"])
		roads = roads.rename_geometry("geom")

		print("uploading batch to PostGIS")

		roads.to_postgis(
			name = "roads",
			con = engine,
			if_exists = "append",
			index = False
		)

		total_inserted += len(roads)
		offset += BATCH_SIZE

		print(f"Inserted rows so far: {total_inserted}")

	print("load_complete")

if __name__ == "__main__":
	load_roads_to_postgis()
