from unittest.mock import mock_open, patch

from src.generators.random_name_generator.RandomNameGenerator import RandomNameGenerator


class TestRandomNameGenerator:
    def setup_method(self):
        RandomNameGenerator._RandomNameGenerator__names_loaded = False
        RandomNameGenerator._RandomNameGenerator__names = []
        RandomNameGenerator._RandomNameGenerator__count = 0

    def test_load_names_reads_json_data(self):
        with patch("builtins.open", mock_open(read_data='{"names": ["Ada", "Linus"], "count": 2}')):
            RandomNameGenerator.load_names()
        assert RandomNameGenerator._RandomNameGenerator__names == ["Ada", "Linus"]
        assert RandomNameGenerator._RandomNameGenerator__count == 2

    def test_generate_loads_names_on_first_call_and_returns_selected_name(self):
        with patch("builtins.open", mock_open(read_data='{"names": ["Ada", "Linus"], "count": 2}')), \
             patch("src.generators.random_name_generator.RandomNameGenerator.randint", return_value=1):
            result = RandomNameGenerator.generate()
        assert result == "Linus"
