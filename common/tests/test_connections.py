"""Test module connections"""
from unittest.mock import patch

from common.connections import postgres_connection


@patch("common.connections.Config")
@patch("common.connections.OsVariable")
@patch("common.connections.create_engine")
def test_postgres_connection(mock_create_engine, *_):
    """Test function postgres_connection"""
    postgres_connection(database="db_yummy")
    assert mock_create_engine.called
