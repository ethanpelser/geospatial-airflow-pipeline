-- Count roads by type
SELECT
	fclass,
	COUNT(*) AS road_count
FROM roads
GROUP BY fclass
ORDER BY road_count DESC;

-- Longest roads in kilometers
SELECT
	name,
	fclass,
	ROUND(ST_LENGTH(geom::geography) / 1000) as road_length
FROM roads
WHERE name IS NOT NULL
ORDER BY road_length
LIMIT 10;

-- Roads closest to Durban city center
SELECT
	name,
	fclass,
	ROUND(
		ST_Distance(
			geom::geography,
			ST_SetSRID(ST_MakePoint(32.0218, -29.8587), 4326):: geography
		)::numeric,
		2
	) AS distance_m
FROM roads
ORDER BY distance_m DESC
LIMIT 10;

-- Count named and unamed roads
SELECT
	CASE
		WHEN name IS NULL THEN 'unamed road'
		ELSE 'named road'
	END AS road_named_status,
	COUNT(*) as road_count
FROM roads
GROUP BY road_named_status;

-- Top 20 longest roads
SELECT
	name,
	fclass,
	ROUND((ST_Length(geom::geography)/1000)::numeric, 2) AS road_length
FROM roads
WHERE name IS NOT NULL
ORDER BY road_length
LIMIT 20;

-- Average road length by road type
SELECT
	fclass,
	ROUND(AVG(ST_Length(geom::geography)/1000)::numeric, 2) as avg_length
FROM roads
GROUP BY fclass
ORDER BY avg_length DESC;

-- Total road length by road type
SELECT
	fclass,
	ROUND(SUM(ST_LENGTH(geom::geography)/1000)::numeric, 2) as sum_length
FROM roads
GROUP BY fclass
ORDER BY sum_length DESC;


