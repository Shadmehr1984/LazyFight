import inspect

import pytest

from src.chests.Chest import Chest


class TestChest:
    def test_chest_is_abstract_and_cannot_be_instantiated(self):
        assert inspect.isabstract(Chest)
        with pytest.raises(TypeError):
            Chest()
