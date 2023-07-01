from typing import List

from rq import Queue
from src.calculator.data.data_access_impl import PGDataAccess
from src.calculator.models.location import Location
from src.database.postgres import PostgresConnection
from src.calculator.calc import calculate_distance
from src.database.redis_mod import RedisConnection

redis_conn = RedisConnection()
connection = redis_conn.get_connection()
task_queue = Queue('distances', connection=connection)

def extract_ids_from_inbound() -> list:
    conn = redis_conn.get_connection()
    id_list = conn.lrange('inbound', -2, -1)
    id_list = [id_.decode() for id_ in id_list]
    return id_list

def locations_dict_to_object(locations: List[dict]) -> List[Location]:
    locations_list = []

    for location in locations:
        loc = Location('', location['name'], location['latitude'], location['longitude'])
        locations_list.append(loc)
    return locations_list

def send_to_outbound():
    conn = redis_conn.get_connection()
    connector = PostgresConnection()
    location = Location('', '', 0, 0)
    data_access = PGDataAccess(connector, location)
    id_list = extract_ids_from_inbound()
    
    locations = data_access.get_locations(id_list)

    locations_to_list = locations_dict_to_object(locations)
    distances = calculate_distance(locations_to_list)
    conn.rpush('outbound', *distances)

    return distances

def send_to_thread():
    job = task_queue.enqueue(send_to_outbound)

    while not job.is_finished:
        job.refresh()
    job_id = job.get_id()
    return job_id
