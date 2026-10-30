import pytest

from src.things.Exceptions.ItemNotEnoughException import ItemNotEnoughException
from src.things.Exceptions.ItemNotExistException import ItemNotExistException


@pytest.mark.parametrize("exception_class", [ItemNotEnoughException, ItemNotExistException])
def test_inventory_exceptions_preserve_message(exception_class):
    error = exception_class("test message")
    assert str(error) == "test message"
