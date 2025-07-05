from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Ajouter le dossier scripts/ au PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Importer les fonctions des scripts
from extract import extract
from transform import transform
from load import load

default_args = {
    'owner': 'randy',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='weather_etl_dag',
    default_args=default_args,
    description='ETL complet pour météo : extract, transform, load',
    schedule_interval='@daily',  # exécuter tous les jours
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['weather', 'ETL'],
) as dag:

    extract_task = PythonOperator(
        task_id='extract_weather_data',
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id='transform_weather_data',
        python_callable=transform,
    )

    load_task = PythonOperator(
        task_id='load_weather_to_gsheet',
        python_callable=load,
    )

    extract_task >> transform_task >> load_task
