from pathlib import Path
import zipfile

RAW_ZIP = Path("data/raw/south-africa-latest-free.shp.zip")
EXTRACT_DIR = Path("data/raw/osm")

def extract_data():
	"""
	Extract the downloaded OpenStreetMap shapefile zip into data/raw/osm
	"""

	EXTRACT_DIR.mkdir(parents=True, exist_ok =True)

	print("Extracting OpenStreetMap shapefile")

	with zipfile.ZipFile(RAW_ZIP, "r") as zip_ref:
		zip_ref.extractall(EXTRACT_DIR)

	print(f"Extracted files to: {EXTRACT_DIR}")

	
if __name__ == "__main__":
	extract_data()
