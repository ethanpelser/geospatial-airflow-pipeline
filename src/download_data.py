from pathlib import Path
import requests
import time
import zipfile

URL = "https://download.geofabrik.de/africa/south-africa-latest-free.shp.zip"

RAW_DIR = Path("data/raw")
OUTPUT_FILE = RAW_DIR / "south-africa-latest-free.shp.zip"


def download_file():
	RAW_DIR.mkdir(parents=True, exist_ok = True)

	print("Download initiated")
	
	for attempt in range(1, 4):
		try:
			response = requests.get(URL, stream=True, timeout=60)
			response.raise_for_status()

			with open(OUTPUT_FILE, "wb") as file:
				for chunk in response.iter_content(chunk_size = 8192):
					file.write(chunk)

			if not zipfile.is_zipfile(OUTPUT_FILE):
				print("Downloaded file is not a ZIP. Retrying...")
				OUTPUT_FILE.unlink(missing_ok=True)
				raise ValueError("Invalid ZIP file")

			print("download complete")
			return

		except (requests.exceptions.RequestException, ValueError) as error:
			print(f"Download failed {error}:")

			if attempt == 3:
				raise
			time.sleep(10)

if __name__ == "__main__":
	download_file()
