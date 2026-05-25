from pathlib import Path
import requests

URL = "https://download.geofabrik.de/africa/south-africa-latest-free.shp.zip"

RAW_DIR = Path("data/raw")
OUTPUT_FILE = RAW_DIR / "south-africa-latest-free.shp.zip"


def download_file():
	RAW_DIR.mkdir(parents=True, exist_ok = True)

	print("Download initiated")
	
	response = requests.get(URL, stream=True)
	response.raise_for_status()

	with open(OUTPUT_FILE, "wb") as file:
		for chunk in response.iter_content(chunk_size = 8192):
			file.write(chunk)

	print("download complete")

if __name__ == "__main__":
	download_file()
