import os

from airflow.models import Variable


class OsVariable: # pylint: disable=too-few-public-methods
    """Os enviroment variable keys"""
    POSTGRES_PASSWORD = "POSTGRES_PASSWORD"


class AirflowVariable: # pylint: disable=too-few-public-methods
    """Airflow varable keys"""
    pass


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
