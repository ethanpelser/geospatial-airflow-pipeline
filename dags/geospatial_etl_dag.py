from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
	"owner": "ethan"
}

with DAG(
    dag_id="geospatial_etl_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

	download_data = BashOperator(
		task_id = "download_data",
		bash_command="cd /opt/airflow && python src/download_data.py"

	)

	create_tables = BashOperator(
	    task_id = "create_tables",
	    bash_command= """
	    docker exec -i geospatial_postgis \
	    psql -U airflow -d geospatial \
	    < /opt/airflow/sql/create_tables.sql
	    """
	)

	load_postgis = BashOperator(
		task_id = "load_postgis",
		bash_command="cd /opt/airflow && python src/load_postgis.py"

	)

	validate_data = BashOperator(
		task_id = "validate_data",
		bash_command="cd /opt/airflow && python src/validate_data.py"
	)

	download_data >> create_tables >> load_postgis >> validate_data
