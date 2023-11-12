"""Test module transformer"""
from unittest.mock import patch, call


import pytest
from pyspark.sql import SparkSession
from services.etl.etl_hr_analytics.transformer import (
    filter_data,
    encrypt_data,
    main,
)


@pytest.fixture(name="spark", scope="session")
def gen_spark_test():
    """Create spark session for test"""
    spark_test = (
        SparkSession.builder.master("local[1]")
        .appName("local-tests")
        .config("spark.executor.cores", "1")
        .config("spark.executor.instances", "1")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
    )
    yield spark_test
    spark_test.stop()


def test_filter_data(spark: SparkSession):  # ignore W0621
    """Test function filter_data"""
    df_test = spark.read.csv(
        path="services/etl/etl_hr_analytics/tests/sample/input_filter_data.csv",
        header=True
    )
    df_result = filter_data(df=df_test)
    assert df_result.count() == 96
    assert len(df_result.columns) == 21


def test_encrypt_data(spark: SparkSession):  # ignore W0621
    """Test function encrypt_data"""
    df_test = spark.read.csv(
        path="services/etl/etl_hr_analytics/tests/sample/input_encrypt_data.csv",
        header=True
    )
    df_expected = spark.read.csv(
        path="services/etl/etl_hr_analytics/tests/sample/expected_encrypt_data.csv",
        header=True
    )
    df_result = encrypt_data(df=df_test)
    assert df_result.count() == 99
    assert df_result.collect() == df_expected.collect()


@patch("services.etl.etl_hr_analytics.transformer.sys.argv", [None, "foo", "ver"])
@patch("services.etl.etl_hr_analytics.transformer.filter_data")
@patch("services.etl.etl_hr_analytics.transformer.encrypt_data")
@patch("services.etl.etl_hr_analytics.transformer.SparkSession")
def test_main(
    mock_spark_session,
    mock_encrypt_data,
    *_
):
    """Test function main"""
    main()
    assert mock_spark_session.builder.master.return_value \
        .appName.return_value \
        .getOrCreate.return_value \
        .read.parquet.call_args_list == [call("foo")]
    assert mock_encrypt_data.return_value \
        .coalesce.call_args_list == [call(numPartitions=1)]
    assert mock_encrypt_data.return_value \
        .coalesce.return_value \
        .write.parquet.call_args_list == [call(path="ver", mode="overwrite")]
