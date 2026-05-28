from pathlib import Path
from sqlalchemmy import create_engine, text

SQL_FILE = Path("sql/create_tables.sql")
DB_URL = "postgresql://airflow:airflow@postgres:5432/geospatial"

def create_table():
	"""
	function to run sql code in order to create roads table
	"""

	IF NOT SQL_FILE.exists():
		raise FileNotFoundError(f"SQL file not found: {SQL_FILE}")

	engine = create_engine(DB_URL)

	with open(SQL_FILE, "r") as file:
		sql = file.read()

	with engine.begin() as conn:
		conn.execute(text(sql))

	print("table created successfully")

if __name__ == "__main__":
	create_table()

