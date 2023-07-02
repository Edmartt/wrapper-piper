from abc import ABC, abstractmethod

from src.calculator.models.location import Location

class AccessDataInterface(ABC):

    @abstractmethod
    def get_location(self, locations_id: str) -> Location | None:
        pass

    @abstractmethod
    def get_locations(self, locations_id: list) -> list:
        pass
