

from flask import jsonify, make_response

from src import calculator


@calculator.calculator_blueprint.errorhandler(401)
def not_authorized(error):
    return make_response(jsonify({'response': 'not authorized'}), 401)


@calculator.calculator_blueprint.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'response': 'bad request'}), 400)
