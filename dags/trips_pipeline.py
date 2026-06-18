from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    "onwer": "gautham",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

def ingest():
    subprocess.run(["python", "src/ingest.py"], check=True)

def load_warehouse():
    subprocess.run(["python", "src/warehouse.py"], check=True)

def run_transforms():
    subprocess.run(["python", "src/run_transforms.py"], check=True)

with DAG(
    dag_id= "nyc_trip_pipeline",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id="ingest", python_callable=ingest)
    t2 = PythonOperator(task_id="load_warehouse", python_callable=load_warehouse)
    t3 = PythonOperator(task_id="run_transforms", python_callable=run_transforms)

    t1 >> t2 >> t3

    