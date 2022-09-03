from multiprocessing import context
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime,timedelta

tables = {'users':
            [{'json_file':'users.json','sql_file':'insert_users.sql'}],
        'subscriptions':
            [{'json_file':'users.json','sql_file':'insert_subscriptions.sql'}],
        'messages':
            [{'json_file':'messages.json','sql_file':'insert_messages.sql'}]
        }
entries = {
    'users':[
        {'http':'https://619ca0ea68ebaa001753c9b0.mockapi.io/',
        'endpoint':'evaluation/dataengineer/jr/v1/users',
        'filename':'users.json'}
    ],
    'messages':[
        {'http':'https://619ca0ea68ebaa001753c9b0.mockapi.io/',
        'endpoint':'evaluation/dataengineer/jr/v1/messages',
        'filename':'messages.json'}
    ]
}

def creating_insert_file(**kwargs):
    from scripts.create_insert_file import CreateInsertData
    if kwargs['table'] == 'users':
        CreateInsertData.create_user_insert_data(kwargs['json_file'],kwargs['sql_file'])
    elif kwargs['table'] == 'subscriptions':
        CreateInsertData.create_subscription_insert_data(kwargs['json_file'],kwargs['sql_file'])
    elif kwargs['table'] == 'messages':
        CreateInsertData.create_messages_insert_data(kwargs['json_file'],kwargs['sql_file'])

def save_file_to_local(**kwargs):
    ti = kwargs['ti']
    from scripts.save_to_local import SaveFile
    SaveFile.save_json_to_file(kwargs['http'],kwargs['endpoint'],kwargs['filename'])

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
    template_searchpath = "/opt/airflow/plugins/sql",
    tags = ['ingestion','api','raw','dbt']
) as dag:

    start = DummyOperator(
        task_id = 'start'
    )

    end = DummyOperator(
        task_id = 'end'
    )

    create_table = PostgresOperator(
        task_id = 'create_raw_tables',
        sql = 'create_tables.sql',
        postgres_conn_id = "POSTGRES_CONNID",
    )

    for topic in entries:

        http_check_sensor = HttpSensor(
            task_id = f'api_{topic}_checker',
            http_conn_id = 'http_xpto_api',
            endpoint = entries[topic][0]['endpoint']
        )

        save_to_local = PythonOperator(
            task_id = f'get_and_save_{topic}_to_local', 
            python_callable = save_file_to_local,
            op_kwargs = {'http':entries[topic][0]['http'] ,'endpoint': entries[topic][0]['endpoint'], 'filename': entries[topic][0]['filename']}
        )

        start >> http_check_sensor >> save_to_local >> create_table

    for table in tables:

        create_sql_insert_file = PythonOperator(
            task_id = f'create_{table}_insert_file',
            python_callable = creating_insert_file,
            op_kwargs = {'table':table ,'json_file': tables[table][0]['json_file'], 'sql_file': tables[table][0]['sql_file']}
        )

        insert_raw = PostgresOperator(
            task_id = f'insert_{table}_raw_data',
            sql = tables[table][0]['sql_file'],
            postgres_conn_id = "POSTGRES_CONNID",
        )

        create_table >> create_sql_insert_file >> insert_raw >> end
