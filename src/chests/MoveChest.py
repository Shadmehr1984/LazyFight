from src.moves.Move import Move
from src.chests.exceptions.NotEnoughMovesForChestException import NotEnoughMovesForChestException
from src.chests.exceptions.ChestAndMovesRankNotSameException import ChestAndMovesRankNotSameException
from src.chests.exceptions.NotEnoughCoinException import NotEnoughCoinException
from src.things.Inventory import Inventory
from random import randint

class MoveChest:
    def __init__(self, rank: int, moves: list[Move]) -> None:
        if (rank < 1):
            raise ValueError(f"invalid rank{rank}")
        if (len(moves) < 3):
            raise NotEnoughMovesForChestException("at least 3 move")
        for move in moves:
            if (rank != move.rank):
                raise ChestAndMovesRankNotSameException("chest rank and all move ranks must be same")
        self.rank = rank
        self.moves = moves
        self.price = 50 + (rank * 100)
    
    def open(self, inventory: Inventory) -> Move:
        try:
            if (inventory.pick_item('coin', self.price)):
                index = randint(0, len(self.moves) - 1)
                move = self.moves[index]
                return move
        except Exception:
            coins = inventory.items.get('coin')
            coins_count = None
            if (coins is None):
                coins_count = 0
            else:
                coins_count = coins.count
            raise NotEnoughCoinException(f'not enough coins, your coins:{coins_count}')
    
    def __str__(self) -> str:
        return f"move chest, rank:{self.rank}, price:{self.price}"