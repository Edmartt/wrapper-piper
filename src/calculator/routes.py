from src.calculator.http_ids_handler import DistanceCalculator
from src.calculator.http_job_handler import Job
from . import calculator_blueprint

calc = DistanceCalculator.as_view('distance calculator')

calculator_blueprint.add_url_rule('/api/v1/locations/ids', view_func=calc, methods=['POST'])

job = Job.as_view('job result')

calculator_blueprint.add_url_rule('/api/v1/locations/distance', view_func=job, methods=['POST'])
