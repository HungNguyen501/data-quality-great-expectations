"""Store connection to data sources"""
from sqlalchemy import create_engine
from common.configs import Config, OsVariable


def postgres_connection(database: str):
    """Create connection to postgres DB
    Args:
        database(str): name of database
    Return connection to the database
    """
    return create_engine(
        url="postgresql+psycopg2://"
        f"{Config.os_get(key=OsVariable.POSTGRES_USER)}:{Config.os_get(key=OsVariable.POSTGRES_PASSWORD)}"
        f"@{Config.os_get(key=OsVariable.POSTGRES_HOST)}:{Config.os_get(OsVariable.POSTGRES_PORT)}/{database}"
    )
