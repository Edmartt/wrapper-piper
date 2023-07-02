from flask import current_app, jsonify, request
from flask.views import MethodView
from src.calculator.data_layer.data_access_interface import AccessDataInterface
from src.calculator.task import send_to_thread
from src.database.redis_mod import RedisConnection

class DistanceCalculator(MethodView):

    def __init__(self, data_access: AccessDataInterface) -> None:
        self.data_access = data_access

    def get(self):
        pass

    def post(self):

        request_data = request.get_json()
        ids = request_data['ids']

        if len(ids) > 2 or len(ids) < 2:
            return jsonify({'response': 'please send two elements at once'}), 400
        existant_ids = self.data_access.get_locations(ids)

        if len(existant_ids) == 0:
            return jsonify({'response': 'ids not found in database'}), 404

        if len(existant_ids) < 2:
            return jsonify({'response': 'some of the ids does not exists'}), 400

        r = RedisConnection()

        r.get_connection().rpush('inbound', *ids)

        with current_app.app_context():
            job_id = send_to_thread()


        return jsonify({'response': {'message': 'ids in the inbound queue', 'JOB ID': job_id}}), 200
