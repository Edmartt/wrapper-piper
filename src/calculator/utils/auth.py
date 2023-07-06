import os
from functools import wraps
from flask import abort, jsonify, request


def is_authorized(func):
    
    @wraps(func)
    def wraps_function(*args, **kwargs):

        auth = request.headers.get('x-api-key')
        auth_env_var = os.environ.get('API_KEY')

        if auth != auth_env_var:
            abort(401, jsonify({'response': 'not authorized'}), 401)
        return func(*args, **kwargs)

    return wraps_function
