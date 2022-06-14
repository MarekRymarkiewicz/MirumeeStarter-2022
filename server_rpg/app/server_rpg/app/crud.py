import http

from database import cursor
from utils import player_to_dict, default_profession_parameters


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


def create_new_player(db, data):
    query = "INSERT INTO players (name, profession, hp, attack_point) VALUES (:name, :profession, :hp, :attack_point)"
    params = {
              "name": data["name"],
              "profession": data["profession"],
              "hp": data["hp"],
              "attack_point": data["attack_points"]
              }

    #TODO: get_player_by_id
    #TODO: handle non-unique name error
    #Use Postman
    #Saleor
    player = db.execute(query, params)
    #Return player as JSON(DICT)
    return player