# Geospatial Airflow ETL Pipeline

## Project Overview

This project is a geospatial data engineering pipeline that uses Apache Airflow, Docker, PostgreSQL/PostGIS, Python, and OpenStreetMap data.

The pipeline downloads OpenStreetMap shapefile data for South Africa, extracts the dataset, creates a PostGIS table, loads road geometry data into PostgreSQL in chunks, and validates the loaded data.

The project is designed as a junior data engineering portfolio project and demonstrates workflow orchestration, Dockerized services, geospatial processing, chunked loading, and spatial SQL analysis.

---

## Tech Stack

- WSL Ubuntu
- Python
- Apache Airflow
- Docker
- Docker Compose
- PostgreSQL
- PostGIS
- Pyogrio
- GeoPandas
- SQLAlchemy
- OpenStreetMap / Geofabrik data

---

## Pipeline Architecture

```text
download_data
    ↓
extract_data
    ↓
create_tables
    ↓
load_postgis
    ↓
validate_data

---

##Project Structure


geospatial-airflow-pipeline/
│
├── dags/
│   └── geospatial_etl_dag.py
│
├── src/
│   ├── download_data.py
│   ├── extract_data.py
│   ├── create_tables.py
│   ├── load_postgis.py
│   └── validate_data.py
│
├── sql/
│   ├── create_tables.sql
│   └── analytical_queries.sql
│
├── data/
│   └── raw/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md

---

##Dataset

The project uses OpenStreetMap shapefile data from Geofabrik:

https://download.geofabrik.de/africa/south-africa-latest-free.shp.zip

This archive contains multiple geospatial layers, including roads, railways, buildings, land use, waterways, places, and points of interest.

This project focuses on:

gis_osm_roads_free_1.shp


---

##Database Table

The main PostGIS table is:

roads


Columns

Column		Description

id		Auto-generated primary key
osm_id		Original OpenStreetMap object ID
code		Numeric road classification
fclass		Road type/class
name		Road name
ref		Road reference number
oneway		Whether the road is one-way
maxspeed	Speed limit
geom		LineString geometry in EPSG:4326

---

##How to Run the Project

1. Clone the repository

</> BASH

git clone <your-repo-url>
cd geospatial-airflow-pipeline

2. Create and activate virtual environment

</> BASH

python3 -m venv venv
source venv/bin/activate

3. Install Python dependencies

</> BASH

pip insall -r requirements.txt

4. Start Docker services

</> BASH
docker compose up --build -d

5. Start the Airflow Scheduler

In a seperate terminal, run:

</> BASH

docker exec -it geospatial_airflow airflow scheduler

Keep this terminal open while running the DAG

6. Open Airflow

In a browser go to http://localhost:8080

login: Username: airflow
       Password: airflow

---

##File Permission Setup

Because Airflow runs inside Docker as a different Linux user, the mounted data/ folder may need permission changes.

Run this from the project root before triggering the DAG

</> BASH

sudo chown -R 50000:0 data
sudo chmod -R 775 data


If you need to edit or delete files locally again, give ownership back to your Ubuntu user:

</> BASH

sudo chown -R 50000:0 data
sudo chmod -R 775 data

---

##Running the DAG

In the Airflow UI:
	1. Open the DAG named: geospatial_etl_pipeline
	2. Trigger the DAG manually!

The DAG will
	1. Download the OpenStreetMap shapefile zip
	2. Extract the shapefile archive
	3. Create the PostGIs table
	4. Load road data into PostGIS table
	5. Validate the loaded data

---

##Chunked Loading

The project loads the shapefile in chunks to avoid memory issues.

Instead of loading the full South Africa roads dataset into RAM at once, load_postgis.py reads a limited number of rows per batch and uploads each batch to PostGIS.

This helps prevent the process from being killed due to high memory usage.

It also only loads the first 10000 entries into the database

---

##Validation Checks

The validation script checks:

total row count
missing geometries
geometry type
SRID
road type counts


---

##Useful commands

Check running containers

</> Bash
docker ps


Start containers

</> Bash

docker compose up -d


Stop containers

</> Bash

docker compose down


Rebuild Airflow image after changing requirements

</> Bash

docker compose build airflow
docker compose up -d


Connect to PostGIS

</> Bash

docker exec -it geospatial_postgis psql -U airflow -d geospatial


---

##Problems Solved

During this project, several real data engineering problems were solved

1. Docker container networking
2. Airflow DAG import errors
3. File permission issues with Docker bind mounts
4. PostGIS version compatability
5. Memory limits when processing large geospatial datasets
6. Chunked shapefile loading
7. Database validation
8. Airflow task orchestration

---

##Possible Future Improvements

Possible future improvements:

Load the full dataset instead of a limited sample
Add spatial indexes for faster queries
Add a dashboard with Streamlit
Store raw data in AWS S3
Add automated tests
Use Airflow connections instead of hardcoded database URLs
Use environment variables for credentials
Add screenshots of successful DAG runs and query results

---

##Author

Ethan Pelser
