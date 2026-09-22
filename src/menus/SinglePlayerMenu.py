from abc import ABC, abstractmethod
from src.creatures.Player import Player

class SinglePlayerMenu(ABC):
    def __init__(self, player: Player) -> None:
        self.player = Player
    
    @abstractmethod
    def open(self) -> bool:
        pass