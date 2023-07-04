from unittest.mock import patch

from src.calculator.task import send_to_thread

def test_send_to_thread():

    with patch('src.calculator.task.task_queue') as mock_queue, patch('src.calculator.task.send_to_outbound') as mock_send_to_outbound:
        
        mock_send_to_outbound.return_value

        job = mock_queue.enqueue.return_value

        expected_id = 'e4574eee-5376-4bbb-9daa-e5d9557cd9c5'

        job.enqueue.return_value
        job.is_finished.return_value = True
        job.get_id.return_value = 'e4574eee-5376-4bbb-9daa-e5d9557cd9c5'
        
        assert send_to_thread() == expected_id
