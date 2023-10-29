"""ETL data with gx for data quality validation"""
import logging

import pandas as pd


def validate_data(data_path: str):
    """Print row count of yellow trip dataset
    Args:
        data_path(str): path of dataset
    """
    df = pd.read_parquet(data_path)
    logging.info(f"Row number of dataset: {df.count()}")
