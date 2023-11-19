"""Unit tests for module alerts"""
from unittest.mock import patch

from common.alerts import (
    airflow_on_failure_callback,
    airflow_sla_miss_callback,
)


@patch("common.alerts.OsVariable")
@patch("common.alerts.Config.os_get")
@patch("common.alerts.Bot")
def test_airflow_on_failure_callback(mock_bot, *_):
    """Test function airflow_on_failure_callback"""
    airflow_on_failure_callback(context={
        "task_instance_key_str": "jack",
    })
    assert mock_bot.called


@patch("common.alerts.OsVariable")
@patch("common.alerts.Config.os_get")
@patch("common.alerts.Bot")
def test_airflow_sla_miss_callback(mock_bot, *_):
    """Test function airflow_on_failure_callback"""
    airflow_sla_miss_callback(
        dag="dummy",
        task_list="dummy",
        blocking_task_list="dummy",
        slas="dummy",
        blocking_tis="dummy",
    )
    assert mock_bot.called
