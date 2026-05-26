from pathlib import Path
import zipfile
import geopandas as gpd

RAW_ZIP = Path("data/raw/south-africa-latest-free.shp.zip")
EXTRACT_DIR = Path("data/raw/osm")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "roads.geojson"

def transform_roads():
	
	"""
	Function that takes road zipfile and cleans it
	"""

	EXTRACT_DIR.mkdir(parents=True, exist_ok = True)
	PROCESSED_DIR.mkdir(parents=True, exist_ok = True)

	print("extracting zipped shapefile")
	with zipfile.ZipFile(RAW_ZIP, "r") as zip_ref:
		zip_ref.extractall(EXTRACT_DIR)
	
	roads_path = EXTRACT_DIR / "gis_osm_roads_free_1.shp"
	
	print("reading roads shapefile")
	
	roads = gpd.read_file(roads_path)
	
	print(f"Original rows {len(roads)}")

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

	roads = roads.dropna(subset =["geometry"])
	roads = roads.to_crs(epsg = "4326")
	
	print(f"Cleaned rows {len(roads)}")
	
	roads.to_file(OUTPUT_FILE, driver = "GeoJSON")
	
	print(f"Saved transformed data to {OUTPUT_FILE}")

if __name__ == "__main__":
	transform_roads()
