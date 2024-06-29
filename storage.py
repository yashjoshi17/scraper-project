from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

class Storage(ABC):
    @abstractmethod
    def save(self, products: List[BaseModel]):
        pass