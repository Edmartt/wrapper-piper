from unittest.mock import patch
from src.calculator.task import extract_ids_from_inbound
from src.calculator import task

def test_extract_ids_from_inbound():
    with patch.object(task, 'redis_conn') as mock_redis_conn:
        mock_conn = mock_redis_conn.get_connection.return_value
        mock_conn.lrange.return_value = [b'12345', b'67890']
        assert extract_ids_from_inbound() == ['12345', '67890']

