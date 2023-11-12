"""Test module dwh_loader"""
from unittest.mock import patch, call

from services.etl.etl_hr_analytics.dwh_loader import load_to_dwh


@patch(
    "services.etl.etl_hr_analytics.dwh_loader.sys.argv",
    [None, "19700101", "dummy_file", "jupyter", "-10", "lisa", "love"])
@patch("services.etl.etl_hr_analytics.dwh_loader.SF")
@patch("services.etl.etl_hr_analytics.dwh_loader.SparkSession")
def test_load_to_dwh(mock_spark_session, mock_sf, *_):
    """Test function load_to_dwh"""
    load_to_dwh()
    mock_spark = mock_spark_session.builder \
        .master.return_value \
        .appName.return_value \
        .getOrCreate.return_value
    assert mock_spark.read.parquet.call_args_list == [call("dummy_file")]
    mock_df = mock_spark.read.parquet.return_value.withColumn
    assert mock_df.call_args_list == [call(colName="ymd", col=mock_sf.lit("19700101"))]
    assert mock_df.return_value.write.mode.call_args_list == [call(saveMode="append")]
    assert mock_df.return_value.write.mode.return_value.format.return_value.options.call_args_list == [
        call(
            url='jdbc:postgresql://jupyter:-10/hr_analytics',
            driver='org.postgresql.Driver',
            user='lisa',
            password='love',
            dbtable='data',
        )
    ]
