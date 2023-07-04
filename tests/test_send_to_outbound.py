from unittest.mock import patch
from src.calculator.task import send_to_outbound
from src.calculator import task


def test_send_to_outbound_integration():

    with patch('src.calculator.task.PostgresConnection') as MockPostgresConnection, patch.object(task, 'redis_conn') as mock_redis_conn, patch('src.calculator.task.extract_ids_from_inbound') as mock_extract_ids_from_inbound, \
        patch('src.calculator.task.PGDataAccess') as MockPGDataAccess:

            mock_conn_redis = mock_redis_conn.get_connection.return_value
            mock_conn_redis.rpush.return_value = 1

            MockPostgresConnection.return_value
            mock_data_access = MockPGDataAccess.return_value

            mock_id_list = mock_extract_ids_from_inbound.return_value = ['123', '456']
            mock_data_access.get_locations.return_value = [{'id':'123', 'name':'location1', 'latitude': 1.23, 'longitude': 2.34}, {'id': '456', 'name': 'location2', 'latitude': 4.56, 'longitude': 5.67}]

            mock_data_access.get_locations(mock_id_list)

            expected = [4.709331162702406]

            result = send_to_outbound()
            assert result == expected
