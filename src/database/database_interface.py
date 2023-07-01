from abc import ABC, abstractmethod
from typing import Optional, Tuple

class IDatabaseConnection(ABC):

    @abstractmethod
    def get_db(self) -> Optional[Tuple]:
        pass

    @abstractmethod
    def close_db(self, e=None) -> None:
        pass
