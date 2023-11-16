"""DAG to etl hr_analytics data"""
from datetime import timedelta
import yaml
import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.models.baseoperator import chain
from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator
)
from common.alerts import airflow_on_failure_callback, airflow_sla_miss_callback
from common.configs import Config, OsVariable
from services.etl.etl_hr_analytics.dwh_aggregation import aggregate_hr_analytics


def load_checkpoint_config(ymd: str) -> dict:
    """Load checkpoint config from file

    Args:
        ymd(str): date to run in format YYYYMMDD

    Returns config as dict
    """
    with open(
        file="services/great_expectations/configs/hr_analytics.yml",
        mode="r",
        encoding="utf-8",
    ) as config_file:
        return yaml.safe_load(config_file.read().format(ymd=ymd))


with DAG(
    dag_id="etl_hr_analytics_data",
    start_date=pendulum.datetime(2023, 10, 28, 0, 0, 0, tz="Asia/Ho_Chi_Minh"),
    schedule="0 2 * * *",
    catchup=False,
    max_active_tasks=1,
    max_active_runs=1,
    tags=["etl", "gx", "hr_analytics",],
    sla_miss_callback=airflow_sla_miss_callback,
) as dag:
    LOGICAL_DATE_NODASH = "{{ dag_run.logical_date.astimezone(dag.timezone) | ds_nodash }}"
    GX_ROOT_DIR = "services/great_expectations"
    ck_kwargs = load_checkpoint_config(ymd=LOGICAL_DATE_NODASH)
    validate_raw_hr_analytics = GreatExpectationsOperator(
        task_id="validate_raw_hr_analytics",
        fail_task_on_validation_failure=True,
        on_failure_callback=airflow_on_failure_callback,
        sla=timedelta(minutes=3),
        data_context_root_dir=GX_ROOT_DIR,
        checkpoint_name="dpd_checkpoint",
        checkpoint_kwargs=ck_kwargs["raw_hr_analytics"],
        return_json_dict=True,
    )
    transform_hr_analytics = SparkSubmitOperator(
        task_id="transform_hr_analytics",
        on_failure_callback=airflow_on_failure_callback,
        sla=timedelta(minutes=30),
        application="services/etl/etl_hr_analytics/transformer.py",
        application_args=[
            f"/opt/airflow/data/raw_zone/hr_analytics/{LOGICAL_DATE_NODASH}",
            f"/opt/airflow/data/clean_zone/hr_analytics/{LOGICAL_DATE_NODASH}",
        ],
        conf={
            "spark.master": "local[*]",
            "spark.driver.memory": "1g",
            "spark.executor.memory": "1g",
            "spark.executor.instances": 1,
            "spark.executor.cores": 1,
        }
    )
    validate_clean_hr_analytics = GreatExpectationsOperator(
        task_id="validate_clean_hr_analytics",
        fail_task_on_validation_failure=True,
        sla=timedelta(minutes=3),
        on_failure_callback=airflow_on_failure_callback,
        data_context_root_dir=GX_ROOT_DIR,
        checkpoint_name="dpd_checkpoint",
        checkpoint_kwargs=ck_kwargs["clean_hr_analytics"],
        return_json_dict=True,
    )
    load_to_dwh = SparkSubmitOperator(
        task_id="load_to_dwh",
        on_failure_callback=airflow_on_failure_callback,
        sla=timedelta(minutes=30),
        application="services/etl/etl_hr_analytics/dwh_loader.py",
        application_args=[
            LOGICAL_DATE_NODASH,
            f"/opt/airflow/data/clean_zone/hr_analytics/{LOGICAL_DATE_NODASH}",
            Config.os_get(OsVariable.POSTGRES_HOST),
            Config.os_get(OsVariable.POSTGRES_PORT),
            Config.os_get(OsVariable.POSTGRES_USER),
            Config.os_get(OsVariable.POSTGRES_PASSWORD),
        ],
        conf={
            "spark.master": "local[*]",
            "spark.driver.memory": "1g",
            "spark.executor.memory": "1g",
            "spark.executor.instances": 1,
            "spark.executor.cores": 1,
            "spark.jars": "libs/postgresql-42.2.2.jar"
        }
    )
    validate_dwh_hr_analytics = GreatExpectationsOperator(
        task_id="validate_dwh_hr_analytics_data",
        sla=timedelta(minutes=3),
        data_context_root_dir=GX_ROOT_DIR,
        fail_task_on_validation_failure=True,
        on_failure_callback=airflow_on_failure_callback,
        checkpoint_name="dpd_checkpoint",
        checkpoint_kwargs=ck_kwargs["dwh_hr_analytics_data"],
        return_json_dict=True,
    )
    agg_hr_analytics = PythonOperator(
        task_id="agg_hr_analytics",
        python_callable=aggregate_hr_analytics,
        depends_on_past=False,
        on_failure_callback=airflow_on_failure_callback,
        retries=0,
        sla=timedelta(minutes=10),
        op_kwargs={
            "ymd": LOGICAL_DATE_NODASH,
        },
    )
    validate_dwh_employee_of_the_year = GreatExpectationsOperator(
        task_id="validate_dwh_employee_of_the_year",
        sla=timedelta(minutes=3),
        data_context_root_dir=GX_ROOT_DIR,
        fail_task_on_validation_failure=True,
        on_failure_callback=airflow_on_failure_callback,
        checkpoint_name="dpd_checkpoint",
        checkpoint_kwargs=ck_kwargs["dwh_employee_of_the_year"],
        return_json_dict=True,
    )
    chain(
        validate_raw_hr_analytics,
        transform_hr_analytics,
        validate_clean_hr_analytics,
        load_to_dwh,
        validate_dwh_hr_analytics,
        agg_hr_analytics,
        validate_dwh_employee_of_the_year,
    )
