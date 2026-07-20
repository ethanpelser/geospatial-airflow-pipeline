# Geospatial Airflow ETL Pipeline

## Overview

This project is an end-to-end geospatial ETL pipeline built with **Apache Airflow**, **Docker**, **PostgreSQL/PostGIS**, and **Python**.

The pipeline downloads OpenStreetMap shapefile data from Geofabrik, extracts the dataset, creates the required PostGIS table, loads road geometries into PostgreSQL in chunks, and validates the imported data.

This project demonstrates several core data engineering concepts, including:

- Workflow orchestration with Apache Airflow
- Dockerized data pipelines
- Geospatial data processing
- Chunked data loading
- Spatial SQL with PostGIS
- ETL pipeline design and validation

---

# Tech Stack

- Python
- Apache Airflow
- Docker
- Docker Compose
- PostgreSQL
- PostGIS
- GeoPandas
- Pyogrio
- SQLAlchemy
- OpenStreetMap (Geofabrik)
- WSL Ubuntu

---

# Pipeline Architecture

```text
download_data
      │
      ▼
extract_data
      │
      ▼
create_tables
      │
      ▼
load_postgis
      │
      ▼
validate_data
```

---

# Project Structure

```text
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
```

---

# Dataset

The project uses OpenStreetMap shapefile data provided by Geofabrik.

Download:

https://download.geofabrik.de/africa/south-africa-latest-free.shp.zip

The archive contains multiple geospatial layers including:

- Roads
- Railways
- Buildings
- Waterways
- Land Use
- Places
- Points of Interest

This project focuses on the road network contained in:

```
gis_osm_roads_free_1.shp
```

---

# Database Schema

The primary PostGIS table created by the pipeline is:

```
roads
```

| Column | Description |
|---------|-------------|
| id | Auto-generated primary key |
| osm_id | OpenStreetMap object ID |
| code | Road classification code |
| fclass | Road type/classification |
| name | Road name |
| ref | Road reference |
| oneway | One-way indicator |
| maxspeed | Speed limit |
| geom | LineString geometry (EPSG:4326) |

---

# How to Run

## 1. Clone the repository

```bash
git clone https://github.com/ethanpelser/geospatial-airflow-pipeline.git
cd geospatial-airflow-pipeline
```

## 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Start Docker

```bash
docker compose up --build -d
```

## 5. Start the Airflow Scheduler

In another terminal:

```bash
docker exec -it geospatial_airflow airflow scheduler
```

Keep this terminal running while executing the DAG.

## 6. Open Airflow

Open your browser and navigate to:

```
http://localhost:8080
```

Default login:

Username:

```
airflow
```

Password:

```
airflow
```

---

# File Permissions

Because Airflow runs inside Docker under a different Linux user, the mounted `data/` directory may require updated permissions.

Before running the DAG:

```bash
sudo chown -R 50000:0 data
sudo chmod -R 775 data
```

To restore ownership to your local Ubuntu user afterwards:

```bash
sudo chown -R $USER:$USER data
```

---

# Running the Pipeline

In the Airflow UI:

1. Open **geospatial_etl_pipeline**
2. Trigger the DAG manually

The pipeline performs the following steps:

1. Download the OpenStreetMap archive
2. Extract the shapefiles
3. Create the PostGIS table
4. Load road geometries into PostgreSQL
5. Validate the imported data

---

# Chunked Loading

The South African road network contains a large number of features.

Instead of loading the entire shapefile into memory, the pipeline processes the data in batches before inserting it into PostgreSQL.

This significantly reduces memory usage and makes the pipeline more scalable.

For demonstration purposes, the current implementation loads the first **10,000** road features.

---

# Validation

The validation script performs several checks after loading the data:

- Total row count
- Missing geometries
- Geometry type
- SRID validation
- Road classification counts

---

# Useful Docker Commands

### View running containers

```bash
docker ps
```

### Start containers

```bash
docker compose up -d
```

### Stop containers

```bash
docker compose down
```

### Rebuild the Airflow image

```bash
docker compose build airflow
docker compose up -d
```

### Connect to PostgreSQL

```bash
docker exec -it geospatial_postgis psql -U airflow -d geospatial
```

---

# Challenges Solved

During development, the project involved solving several real-world engineering problems:

- Docker networking
- Airflow DAG import issues
- Docker file permission problems
- PostgreSQL/PostGIS version compatibility
- Processing large geospatial datasets
- Chunked shapefile loading
- Database validation
- Airflow workflow orchestration

---

# Future Improvements

Potential enhancements include:

- Load the complete road dataset
- Add spatial indexes for improved query performance
- Integrate AWS S3 for raw data storage
- Configure Airflow Connections instead of hardcoded connection strings
- Store credentials in environment variables
- Add automated unit and integration tests
- Build a Streamlit dashboard
- Include screenshots of DAG runs and query results

---

# Author

**Ethan Pelser**
