import os
from redis import Redis
import redis


class RedisConnection:

    def __init__(self) -> None:
        self.host = os.environ.get('REDIS_HOST') or 'localhost'
        self.port = os.environ.get('REDIS_PORT') or 6379
        self.password=os.environ.get('REDIS_PASSWORD')

    def get_connection(self) -> Redis:

        redis_conn = redis.StrictRedis(
                host=self.host,
                port=int(self.port),
                password=self.password
                )

        return redis_conn

    def close_connection(self, e=None):
        conn = self.get_connection()
        conn.close()


red = RedisConnection()

def init_app(app):
    app.teardown_appcontext(red.close_connection)
