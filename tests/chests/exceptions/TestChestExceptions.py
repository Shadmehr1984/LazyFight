import pytest

from src.chests.exceptions.ChestAndMovesRankNotSameException import ChestAndMovesRankNotSameException
from src.chests.exceptions.NotEnoughCoinException import NotEnoughCoinException
from src.chests.exceptions.NotEnoughItemsForChestException import NotEnoughItemsForChestException
from src.chests.exceptions.NotEnoughMovesForChestException import NotEnoughMovesForChestException
from src.chests.exceptions.NotValidItemCountException import NotValidItemCountException


@pytest.mark.parametrize("exception_class", [
    ChestAndMovesRankNotSameException,
    NotEnoughCoinException,
    NotEnoughItemsForChestException,
    NotEnoughMovesForChestException,
    NotValidItemCountException,
])
def test_chest_exceptions_preserve_message(exception_class):
    error = exception_class("test message")
    assert str(error) == "test message"
