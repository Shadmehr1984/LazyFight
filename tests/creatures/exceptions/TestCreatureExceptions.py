import pytest

from src.creatures.exceptions.NameIsToBigException import NameIsToBigException
from src.creatures.exceptions.NameIsToSmallException import NameIsToSmallException
from src.creatures.exceptions.NotEnoughMovesException import NotEnoughMoveException


@pytest.mark.parametrize("exception_class", [
    NameIsToBigException,
    NameIsToSmallException,
    NotEnoughMoveException,
])
def test_creature_exceptions_preserve_message(exception_class):
    error = exception_class("test message")
    assert str(error) == "test message"
