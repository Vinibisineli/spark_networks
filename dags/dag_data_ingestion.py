from multiprocessing import context
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python_operator import PythonOperator

from datetime import datetime,timedelta

entries = ['users','messages']
entries_aux = {
    'users':[
        {'endpoint':'evaluation/dataengineer/jr/v1/users',
        'filename':'users.json'}
    ],
    'messages':[
        {'endpoint':'evaluation/dataengineer/jr/v1/messages',
        'filename':'messages.json'}
    ]
}

def save_file_to_local(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(key='return_value', task_ids=kwargs['pti'])
    #print(data)
    from scripts.save_to_local import SaveFile
    SaveFile.save_json_to_file(data,kwargs['filename'])

default_args = {
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'provide_context': True,
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

    end = DummyOperator(
        task_id = 'end'
    )

    for topic in entries:

        http_check_sensor = HttpSensor(
            task_id=f'api_{topic}_checker',
            http_conn_id='http_xpto_api',
            endpoint=entries_aux[topic][0]['endpoint']
        )

        http_get = SimpleHttpOperator(
            task_id=f'api_{topic}_get',
            http_conn_id='http_xpto_api',
            method='GET',
            endpoint=entries_aux[topic][0]['endpoint']
        )

        save_to_local = PythonOperator(
            task_id=f'save_{topic}_to_local', 
            python_callable=save_file_to_local,
            op_kwargs={'pti': http_get.task_id, 'filename': entries_aux[topic][0]['filename']}
        )

        start >> http_check_sensor >> http_get >> save_to_local >> end








    # start >> [http_user_check_sensor,http_message_check_sensor] 
    # http_user_check_sensor >> http_user_get >> save_to_local >> end
    # http_message_check_sensor >> http_message_get >> save_to_local >> end

    