# Geospatial Airflow ETL Pipeline

This project is a junior data engineering portfolio project that builds an automated ETL pipeline for geospatial data.

## Tech Stack

- WSL Ubuntu
- Python
- Apache Airflow
- Docker
- PostgreSQL
- PostGIS
- GeoPandas
- OpenStreetMap data

## Project Goal

The goal of this project is to download OpenStreetMap geospatial data, transform it with Python, load it into PostgreSQL/PostGIS, and run spatial analysis queries.

## Pipeline Steps

1. Download geospatial data
2. Extract and clean road data
3. Transform geometry data
4. Load cleaned data into PostGIS
5. Run validation checks
6. Run spatial SQL analysis
7. Orchestrate the pipeline with Airflow
