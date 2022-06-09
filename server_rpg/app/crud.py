import http

from database import cursor
from utils import player_to_dict

def get_players(db):
    results = []
    query = "SELECT rowid, name, profession, hp, attack_point, status, deaths, kills FROM players"

    for player in db.execute(query):
        player_data = player_to_dict(*player)
        results.append(player_data)

    return results

def get_player_by_name(db, player_name):
    query = "SELECT rowid, name, profession, hp, attack_point, status, deaths, kills FROM players WHERE name =:name COLLATE NOCASE"
    params = {"name": player_name,}
    player = db.execute(query, params).fetchone()
    if not player:
        return None
    return player_to_dict(*player)
