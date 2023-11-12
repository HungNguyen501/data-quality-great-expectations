"""Config os vars and airflow vars as well"""
import os

from airflow.models import Variable


class OsVariable:  # pylint: disable=too-few-public-methods
    """Os enviroment variable keys"""
    POSTGRES_HOST = "POSTGRES_HOST"
    POSTGRES_PORT = "POSTGRES_PORT"
    POSTGRES_USER = "POSTGRES_USER"
    POSTGRES_PASSWORD = "POSTGRES_PASSWORD"
    TELEGRAM_API_TOKEN = "TELEGRAM_API_TOKEN"
    TELEGRAM_CHAT_ID = "TELEGRAM_CHAT_ID"


class AirflowVariable:  # pylint: disable=too-few-public-methods
    """Airflow varable keys"""
    VAR_TEST = "VAR_TEST"


class Config:  # pylint: disable=too-few-public-methods
    """ Config """

    @staticmethod
    def os_get(key):
        """Get os' env variable
        Args:
            key(str):
        Returns:
            variable value
        """
        return os.getenv(key)

    @staticmethod
    def airflow_get(key):
        """Get airflow's variable
        Args:
            key(str):
        Returns:
            variable value
        """
        return Variable.get(key)
