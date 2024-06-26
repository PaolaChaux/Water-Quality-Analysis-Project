from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain
from datetime import datetime
import etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 29),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}


with DAG(
    'Proyect_Water',
    default_args=default_args,
    description='Our dag_water',
    schedule_interval='@daily',  
) as dag:



    read_api = PythonOperator(
        task_id='extract_api',
        python_callable=etl.extract_api,
        provide_context=True,
    )
    

    transform_api = PythonOperator(
        task_id='transform_api',
        python_callable=etl.transform_api,
        provide_context=True,
    )
    
    
    validate_api = PythonOperator(
        task_id='expectation_api',
        python_callable=etl.expectation_api,
        provide_context=True,
    )    


    read_water = PythonOperator(
        task_id='read_water',
        python_callable=etl.read_water,
        provide_context=True,
    )
    
    
    transform_water = PythonOperator(
        task_id='transform_water',
        python_callable=etl.transform_water,
        provide_context=True,
    )
    
    
    validate_water  = PythonOperator(
        task_id='expectation_water',
        python_callable=etl.expectation_water,
        provide_context=True,
    )
    


    merge_task = PythonOperator(
        task_id='merge',
        python_callable=etl.merge_task,
        provide_context=True,
    )
    
    
    load_task = PythonOperator(
        task_id='load_task',
        python_callable=etl.load,
        provide_context=True,
    )
    
    kafka_stream_task = PythonOperator(
    task_id= 'stream_data',
    python_callable = etl.stream_data,
    provide_context = True
    )

    
    read_water >> transform_water >> validate_water 
    read_api >> transform_api >> validate_api
    [validate_water , validate_api] >> merge_task >> load_task >> kafka_stream_task


   

  
