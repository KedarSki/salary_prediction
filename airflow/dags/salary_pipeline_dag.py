import os

from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from dotenv import load_dotenv
from src.pipelines_airflow.oracle_loader import load_jobs_from_csv
from src.pipelines_airflow.data_fetcher import download_csv_from_url


load_dotenv()

default_args = {"owner": "airflow", "retries": 1, "retry_delay": timedelta(minutes=5)}

with DAG(
    dag_id="load_jobs_to_oracle",
    default_args=default_args,
    description="Load cleaned job data to Oracle table",
    schedule_interval=None,
    start_date=datetime(2025, 4, 1),
    catchup=False,
) as dag_load:

    def run_loader():
        csv_path = Path(os.getenv("CLEANED_DATA_PATH"))
        load_jobs_from_csv(csv_path)

    load_task = PythonOperator(task_id="load_jobs_task", python_callable=run_loader)

with DAG(
    dag_id="download_data_task",
    default_args=default_args,
    description="Download CSV file from ovh server",
    schedule_interval=None,
    start_date=datetime(2025, 4, 1),
    catchup=False,   
) as dag_download:

    def run_fetcher():
        url = Path(os.getenv("DATA_SOURCE"))
        output_path = Path(os.getenv("OUTPUT_PATH"))
        download_csv_from_url(url, output_path)
    
    load_task = PythonOperator(task_id="fetch_csv_file", python_callable=run_fetcher)