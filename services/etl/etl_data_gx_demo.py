"""ETL data with gx for data quality validation"""
import logging

import pandas as pd
from sqlalchemy import create_engine
from common.configs import Config


def capture_user_data():
    """
        Print row count of user data
    """
    conn_string = f"postgresql+psycopg2://airflow:{Config.os_get(key='POSTGRES_PASSWORD')}@postgres:5432/hungnd8"
    postgres_conn = create_engine(conn_string)
    df = pd.read_sql(
        con=postgres_conn,
        sql="select * from public.user"
    )
    logging.info(f"total rows is {df.shape}")


def capture_yellow_trip_data(data_path: str):
    """Print row number of dataset
    Args:
        data_path(str): path of dataset
    """
    df = pd.read_parquet(path=data_path)
    logging.info(f"{df.shape}")
