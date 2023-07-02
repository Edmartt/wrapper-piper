from src.calculator.http_ids_handler import DistanceCalculator
from src.calculator.data_layer.data_access_impl import PGDataAccess
from src.calculator.models.location import Location
from src.database.postgres import PostgresConnection
from src.calculator.http_job_handler import Job
from . import calculator_blueprint

location = Location('', '', 0, 0)
connector = PostgresConnection()
data_access = PGDataAccess(connector, location)

calc = DistanceCalculator.as_view('distance calculator', data_access)

calculator_blueprint.add_url_rule('/api/v1/locations/ids', view_func=calc, methods=['POST'])

job = Job.as_view('job result')

calculator_blueprint.add_url_rule('/api/v1/locations/distance', view_func=job, methods=['POST'])
