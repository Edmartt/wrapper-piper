from unittest.mock import patch
from pytest import raises

from flask import Flask
from werkzeug.exceptions import HTTPException

from src.calculator.utils.auth import is_authorized

app = Flask(__name__)
mock_headers = {'x-api-key': 'test_key'}
mock_env_var = 'test_key'

@is_authorized
def mock_is_authorized():
    return 'authorized'

def test_is_authorized():
    with app.test_request_context(headers=mock_headers):

        with patch.dict('os.environ', {'API_KEY': mock_env_var}):

            response = mock_is_authorized()

            assert response == 'authorized'

def test_is_not_authorized():

    with app.test_request_context(headers={'x-api-key': 'wrong_key'}):
        with patch.dict('os.environ', {'API_KEY': mock_env_var}):
            with raises(HTTPException) as ex:
                mock_is_authorized()
                assert ex.value.code == 401
