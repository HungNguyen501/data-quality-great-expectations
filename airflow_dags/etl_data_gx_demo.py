"""DAG to etl yellow_trip data"""
from datetime import timedelta
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain
from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator
)
from services.etl.etl_data_gx_demo import (
    capture_user_data,
    capture_yellow_trip_data,
)


with DAG(
    dag_id="etl_data_gx_demo",
    description="etl yellow trip data",
    tags=["etl", "gx", "demo"],
    start_date=pendulum.datetime(2023, 10, 28, 0, 0, 0, tz="Asia/Ho_Chi_Minh"),
    schedule="0 2 * * *",
    catchup=False,
    max_active_tasks=3,
    max_active_runs=1,
):
    validate_user_data = GreatExpectationsOperator(
        task_id="validate_user_data",
        data_context_root_dir="services/great_expectations",
        checkpoint_name="user",
        fail_task_on_validation_failure=True,
        return_json_dict=True,
    )
    etl_user_data = PythonOperator(
        task_id="etl_user_data",
        python_callable=capture_user_data,
        depends_on_past=False,
        retries=0,
        execution_timeout=timedelta(minutes=10),
    )
    validate_yellow_trip_data = GreatExpectationsOperator(
        task_id="validate_yellow_trip_data",
        data_context_root_dir="services/great_expectations",
        checkpoint_name="yellow_trip_data",
        fail_task_on_validation_failure=True,
        return_json_dict=True,
    )
    etl_yellow_trip_data = PythonOperator(
        task_id="etl_yellow_trip_data",
        python_callable=capture_yellow_trip_data,
        depends_on_past=False,
        retries=0,
        op_kwargs={
            "data_path": "data/yellow_tripdata_2009-12.parquet",
        },
    )
    validate_yellow_trip_data_with_spark = GreatExpectationsOperator(
        task_id="validate_yellow_trip_data_with_spark",
        data_context_root_dir="services/great_expectations",
        checkpoint_name="yellow_trip_data_with_spark",
        fail_task_on_validation_failure=True,
        return_json_dict=True,
    )
    chain(
        validate_user_data,
        etl_user_data,
    )
    chain(
        validate_yellow_trip_data,
        etl_yellow_trip_data,
    )
