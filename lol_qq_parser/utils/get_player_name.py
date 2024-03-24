from lol_qq_parser.utils import query_tjstats
from lol_qq_parser.utils import Endpoints

player_names_cache = {}


def get_player_name(player_id, season_id):
    # Sometimes the match detail file contains playerId = 0 which makes the query fail
    if player_id == 0:
        return None
    if player_id in player_names_cache:
        return player_names_cache[player_id]
    player_data_url = Endpoints.get_player_data_url(season_id, player_id)
    player_data = query_tjstats(player_data_url)
    player_names_cache[player_id] = player_data["data"][0]["playerName"] or None
    return player_names_cache[player_id]
