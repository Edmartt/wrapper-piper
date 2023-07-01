from flask import Blueprint

calculator_blueprint = Blueprint('calculator bp', __name__)

from . import routes
