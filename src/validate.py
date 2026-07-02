from sqlalchemy import create_engine, text
from config import DATABASE_URL

def validate_data():
	engine = create_engine(DATABASE_URL)
	
	checks = {
		"row_count": """
			SELECT COUNT(*) FROM roads;
		""",
		"missing_geometry": """
			SELECT COUNT(*) FROM roads
			WHERE geom IS NULL;
		""",
		"geometry_type": """
			SELECT DISTINCT GeometryType(geom) FROM roads;
		""",
		"srid": """
			SELECT DISTINCT ST_SRID(geom) FROM roads;
		""",
		"road_types_by_amount": """
			SELECT fclass, COUNT(*) AS road_count
			FROM roads
			GROUP BY fclass
			ORDER BY road_count DESC
			LIMIT 10;
		""",
	}
		
	with engine.connect() as conn:
		for check_name, query in checks.items():
			print(f"\n---{check_name}---")
			result = conn.execute(text(query)).fetchall()

			for row in result:
				print(row)

if __name__ == "__main__":
	validate_data()
