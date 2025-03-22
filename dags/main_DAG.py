# enter logic that returns a df and uploads it to the postgres db
from airflow import DAG
from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import dags.scraper as scraper

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    default_args=default_args,
    schedule_interval=timedelta(hours=1),  # Set the schedule to hourly using timedelta
    catchup=False,  # Do not perform a backfill of missing runs
    description='An example DAG that runs hourly using timedelta',
)
def hourly_dag_with_timedelta():

    @task
    def extract() -> pd.DataFrame:
        data = scraper.get_listings()
        return data

    @task
    def transform(df:pd.DataFrame):
        df["age"] = pd.to_datetime(df["age"], format="%m-%Y")
        arr = df.replace([np.nan], [None]).to_numpy()
        data_tuples = [tuple(row) for row in arr]
        return data_tuples
    
    @task
    def load(data:tuple):
        SQLExecuteQueryOperator(
            task_id='load_data_to_postgres',
            conn_id='postgres_default',
            sql="""
            INSERT INTO car_data (guid, price, make, model, mileage, fuel_type, age, transmission)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (guid) DO NOTHING;
            """,
            parameters=data
        ).execute(context={})
        
    # Call the task to include it in the DAG
    extracted_data = extract()
    prepared_data = transform(extracted_data)
    load(prepared_data)

# Call the DAG function to define the DAG
dag = hourly_dag_with_timedelta()
