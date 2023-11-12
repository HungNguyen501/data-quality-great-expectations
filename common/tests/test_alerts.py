"""Unit tests for module alerts"""
from unittest.mock import patch

import pytest
from common.alerts import (
    dpd_alert,
    airflow_on_failure_callback,
    airflow_sla_miss_callback,
)


@patch("common.alerts.OsVariable")
@patch("common.alerts.Config.os_get")
@patch("common.alerts.Bot")
def test_dpd_alert(mock_bot, *_):
    """Test function dpd_alert"""
    @dpd_alert(alert_name="firing", suppress=False)
    def func():
        """dummy function"""
        raise ValueError("ding")

    @dpd_alert(alert_name="firing", suppress=True)
    def func_suppress():
        """dummy supress function"""
        raise ValueError("dong")

    with pytest.raises(ValueError):
        func()
    func_suppress()
    assert mock_bot.return_value.send_message.call_count == 2


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
    airflow_sla_miss_callback(context={
        "task_instance_key_str": "jack",
    })
    assert mock_bot.called
