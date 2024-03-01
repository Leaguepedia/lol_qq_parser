from lol_qq_parser.utils import query_tjstats
from lol_qq_parser.utils import Endpoints


def get_player_name(player_id, season_id):
    player_data_url = Endpoints.get_player_data_url(season_id, player_id)
    player_data = query_tjstats(player_data_url)
    return player_data["data"][0]["playerName"]