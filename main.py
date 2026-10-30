from src.models.PlayerModel import PlayerModel
from src.menus.MainMenu import MainMenu

players = PlayerModel.load_all_players()

(MainMenu(players)).open()