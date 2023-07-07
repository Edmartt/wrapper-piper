from typing import Any, Dict, List
from flask import Flask, request
import pytest
from src.calculator.data_layer.data_access_interface import AccessDataInterface

from src.calculator.http_ids_handler import DistanceCalculator
from src.calculator.models.location import Location


app = Flask(__name__)

class MockDataAccess(AccessDataInterface):

    def get_location(self, locations_id: str) -> Location:
        return Location('', '', 0, 0)

    def get_locations(self, ids: Dict[str, List[Dict[str, str]]]):
        return [{}]

@pytest.mark.parametrize(
        "ids_list, expected_response",
        [(['123'], 2),
         (['456', '789', '012'], 2),
         (['101','102', '103', '104'], 2)
         ]
        )

def test_http_post_len_is_not_2(ids_list: Dict[str, List[str]], expected_response: int):
    with app.test_request_context(json=ids_list):
        request_data = request.get_json()
        assert len(request_data) != expected_response

def test_http_len_ids_not_two():

    mock_data_access = MockDataAccess()
    calc = DistanceCalculator(mock_data_access)

    with app.test_request_context(json={'ids': ['123']}):
        response_message = calc.post()[0].get_json()
        response_code = calc.post()[1]
        
        assert response_message == {'response': 'please send two elements at once'}
        assert response_code == 400

def test_http_post_ids_not_exists():

    mock_data_access = MockDataAccess()

    calc = DistanceCalculator(mock_data_access)

    with app.test_request_context(json={'ids': ['123', '456']}):

        response_message = calc.post()[0].get_json()
        response_code = calc.post()[1]

        assert response_message == {'response': 'some of the ids does not exists'}
        assert response_code == 400
