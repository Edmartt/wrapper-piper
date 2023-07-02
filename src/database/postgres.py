import logging
import os
import traceback
import psycopg2
from psycopg2.extras import RealDictCursor

from src.database.database_interface import IDatabaseConnection

class PostgresConnection(IDatabaseConnection):

    def get_db(self):
        try:
            connection  = psycopg2.connect(
                    database=os.environ.get('PG_DATABASE'),
                    host=os.environ.get('PG_HOST'),
                    user=os.environ.get('PG_USER'),
                    password=os.environ.get('PG_PASSWORD'),
                    port=os.environ.get('PG_PORT')
                    )

            logging.warning(
                    str({
                        'connection open when 0': connection.closed
                        })

                    )

            cursor = connection.cursor(cursor_factory=RealDictCursor)
            return connection, cursor
        except psycopg2.OperationalError:
            logging.error(traceback.format_exc())

    def close_db(self, e=None) -> None:
        db_connect, _ = self.get_db()       

        if db_connect is not None:
            db_connect.close()

connector = PostgresConnection()

def init_app(app) -> None:
    app.teardown_appcontext(connector.close_db)
