""" Unit test for configs module """
from unittest.mock import patch
from common.configs import Config


@patch("os.getenv", return_value='dummy')
def test_os_get(_):
    """ test Config's os_get function """
    assert Config.os_get("foo") == 'dummy'


@patch("common.configs.Variable.get", return_value='dummy')
def test_airflow_get(_):
    """ test Config's os_get function """
    assert Config.airflow_get("foo") == 'dummy'
