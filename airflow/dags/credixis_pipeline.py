import sys 
sys.path.insert(0, "/opt/airflow")
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.data_loader import load_data, validate_data


def validate_transactions():
    df = load_data()
    validate_data(df)


with DAG(
    dag_id="credixis_pipeline",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
) as dag:

    validate_task = PythonOperator(
        task_id="validate_transactions",
        python_callable=validate_transactions,
    )