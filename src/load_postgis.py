import pyogrio
from sqlalchemy import create_engine, text

DB_URL = "postgresql://airflow:airflow@localhost:5432/geospatial"
DATA_PATH = "data/processed/roads.geojson"
MAX_ROWS = 10000
BATCH_SIZE = 2000

def load_data_in_chunks():
	"""
	loads the geospatial data into database in chunks 
	MAX_ROWS is the amount of rows you want to load
	BATCH_SIZE is the amount of rows in each chunk 
	"""

	print("Connecting to PostGis database")
	engine = create_engine(DB_URL)
	
	print("clearing existing table data")
        
	with engine.begin() as conn:
                conn.execute(text("TRUNCATE TABLE roads;"))
	
	print("opening geojson file")
	
	offset = 0
	total_inserted = 0

	while total_inserted < MAX_ROWS:
		
		print(f"Reading rows {offset} to {offset + BATCH_SIZE}")
	
		gdf = pyogrio.read_dataframe(
			DATA_PATH,
			skip_features = offset,
			max_features = BATCH_SIZE
		)

		if gdf.empty:
			break

		gdf = gdf[
			[
				"osm_id",
				"code",
				"fclass",
				"name",
				"ref",
				"oneway",
				"maxspeed",
				"geometry"
			]
		]

		gdf = gdf.to_crs(epsg = 4326)

		gdf = gdf.rename(columns = {"geometry": "geom"})

		gdf = gdf.set_geometry("geom")

		print("uploading batch")

		
		gdf.to_postgis(
			name = "roads",
			con = engine,
			if_exists = "append",
			index = False
		)

		total_inserted += len(gdf)
		print(f"Rows inserted so far: {total_inserted}")
		offset += BATCH_SIZE
	print("chunked load complete")



if __name__ == "__main__":
	load_data_in_chunks()
