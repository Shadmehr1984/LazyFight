from abc import ABC, abstractmethod
from src.things.Inventory import Inventory

class Chest(ABC):
    @abstractmethod
    def open(self, inventory: Inventory):
        pass