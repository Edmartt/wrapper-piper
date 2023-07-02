from flask import Blueprint

calculator_blueprint = Blueprint('calculator_bp', __name__)

from . import routes, http_ids_handler, calc, http_job_handler
