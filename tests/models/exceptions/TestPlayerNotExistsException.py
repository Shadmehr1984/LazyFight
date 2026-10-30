from src.models.exceptions.PlayerNotExistsException import PlayerNotExistsException


class TestPlayerNotExistsException:
    def test_exception_preserves_message(self):
        error = PlayerNotExistsException("player does not exist")
        assert str(error) == "player does not exist"
