"""DAG to etl yellow_trip data"""
from datetime import timedelta
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
from services.etl.etl_yellow_trip_data import validate_data


with DAG(
    dag_id="etl_yellow_trip_data",
    description="etl yellow trip data",
    tags=["etl"],
    start_date=pendulum.datetime(2023, 10, 28, 0, 0, 0, tz="Asia/Ho_Chi_Minh"),
    schedule=None,
    catchup=False,
    max_active_tasks=1,
    max_active_runs=1,
):
    # yellow_trip_data_validation = GreatExpectationsOperator(
    #     task_id="yellow_trip_data_validation",
    #     data_context_config="great_expectations",
    #     checkpoint_name="yellow_trip_data_validation",
    #     fail_task_on_validation_failure=True,
    # )
    etl_yellow_trip_data = PythonOperator(
        task_id="etl_yellow_trip_data",
        python_callable=validate_data,
        depends_on_past=False,
        retries=0,
        execution_timeout=timedelta(minutes=10),
        op_kwargs={
            "data_path": "data/yellow_tripdata_2009-12.parquet",
        },
    )
