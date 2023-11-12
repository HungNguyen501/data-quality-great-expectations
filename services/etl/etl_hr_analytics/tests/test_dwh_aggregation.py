"""Test moudle dwh_aggregation"""
from unittest.mock import patch, call

from services.etl.etl_hr_analytics.dwh_aggregation import aggregate_hr_analytics


@patch("services.etl.etl_hr_analytics.dwh_aggregation.postgres_connection")
def test_aggregate_hr_analytics(mock_postgres_conn, *_):
    """Test function aggregate_hr_analytics"""
    aggregate_hr_analytics(ymd="19700101")
    assert mock_postgres_conn.call_args_list == [call(database="hr_analytics")]
    assert mock_postgres_conn.return_value.connect.execute
