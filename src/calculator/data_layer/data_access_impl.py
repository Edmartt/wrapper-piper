import logging
import traceback
import psycopg2
import psycopg2.errors
from typing import List
from .data_access_interface import AccessDataInterface
from ..models.location import Location
from src.database.database_interface import IDatabaseConnection


class PGDataAccess(AccessDataInterface):
    
    def __init__(self, connector: IDatabaseConnection, location: Location) -> None:
        self.connector = connector
        self.location = location

    def get_location(self, location_id) -> Location | None:
        connection, cursor = self.connector.get_db()
        query = '''
                SELECT * FROM locations WHERE id = %s
                '''

        try:
            cursor.execute(query, (location_id,))
            result = cursor.fetchone()

            if result is not None:
                self.location.location_id = result['id']
                self.location.name = result['name']
                self.location.latitude = result['latitude']
                self.location.longitude = result['longitude']
                connection.commit()
                return self.location

        except psycopg2.ProgrammingError:
            logging.error(traceback.format_exc())
            return None

        finally:
            cursor.close()
            self.connector.close_db()


    def get_locations(self, locations_id: List[dict]) -> List[dict]:
        connection, cursor = self.connector.get_db()

        query = '''
        SELECT * FROM locations WHERE id IN %s
        '''
        params = (tuple(locations_id),)
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()

            locations = []

            if results:

                for row in results:
                    locations_dict = {'name': row['name'], 'longitude': row['longitude'], 'latitude': row['latitude']}
                    locations.append(locations_dict)
                connection.commit()

            return locations

        except psycopg2.ProgrammingError:
            logging.exception((traceback.print_exc()))
            return [{'error': 'Internal error ocurred'}]
        except psycopg2.errors.InvalidTextRepresentation:
            logging.exception(traceback.print_exc())
            return [{'error': 'uuid format invalid'}]

        finally:
            cursor.close()
            connection.close()
