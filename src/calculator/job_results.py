import logging
import traceback
from rq import Queue
from rq.job import Job
from rq.exceptions import NoSuchJobError

from src.database.redis_mod import RedisConnection


redis_object = RedisConnection()

redis_conn = redis_object.get_connection()
queue = Queue('distances', connection=redis_conn)

def get_job_result(job_id: str):
    try:
        job = Job.fetch(job_id, connection=queue.connection)
        if job.is_finished:
            return job.result
        return None
    except NoSuchJobError:
        logging.exception(traceback.print_exc())
