from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.http.operators.http import SimpleHttpOperator

from datetime import datetime,timedelta

default_args = {
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id = 'spark_etl',
    schedule_interval = None,
    start_date = datetime(2022, 9, 1),
    catchup = False,
    tags = ['ingestion','api','raw','dbt']
) as dag:

    start = DummyOperator(
        task_id = 'start'
    )

    http_user_check_sensor = SimpleHttpOperator(
        task_id='api_user_checker',
        http_conn_id='http_xpto_api',
        method='GET',
        endpoint='evaluation/dataengineer/jr/v1/users'
    )

    http_message_check_sensor = SimpleHttpOperator(
        task_id='api_message_checker',
        http_conn_id='http_xpto_api',
        method='GET',
        endpoint='evaluation/dataengineer/jr/v1/messages'
    )

    end = DummyOperator(
        task_id = 'end'
    )

    start >> [http_user_check_sensor,http_message_check_sensor] >> end