from unittest.mock import patch

from src.generators.ItemGenerator import ItemGenerator


class TestItemGenerator:
    def test_generate_returns_item_with_five_count(self):
        with patch("src.generators.ItemGenerator.randint", return_value=0) as random_index:
            item = ItemGenerator.generate()
        random_index.assert_called_once_with(0, 9)
        assert item.name == "fire-token"
        assert item.count == 5

    def test_generate_maps_last_index_to_last_available_name(self):
        with patch("src.generators.ItemGenerator.randint", return_value=9):
            item = ItemGenerator.generate()
        assert item.name == "oil"
        assert item.count == 5
