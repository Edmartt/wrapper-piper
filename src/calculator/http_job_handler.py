from flask import jsonify, request
from flask.views import MethodView

from src.calculator.utils.auth import is_authorized
from .job_results import get_job_result


class Job(MethodView):

    decorators = [is_authorized]
    def __init__(self) -> None:
        pass

    def post(self):
        request_data = request.get_json()
        job_id = request_data.get('job_id', None)

        if job_id is None:
            return jsonify({'response': 'missing job id'}), 400
        job_result = get_job_result(job_id)
        return jsonify({'response': {'distance': job_result, 'message':'job finished'}}), 200
