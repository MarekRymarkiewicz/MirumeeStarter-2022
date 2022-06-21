import http
import sqlite3
from database import cursor
from utils import player_to_dict, default_profession_parameters


def get_players(db):
    results = []
    query = "SELECT rowid, name, profession, hp, attack_points, status, deaths, kills FROM players"

    for player in db.execute(query):
        player_data = player_to_dict(*player)
        results.append(player_data)

    return results


def get_player_by_name(db, player_name):
    query = "SELECT rowid, name, profession, hp, attack_points, status, deaths, kills FROM players WHERE name =:name COLLATE NOCASE"
    params = {"name": player_name, }
    player = db.execute(query, params).fetchone()

    if not player:
        return None
    return player_to_dict(*player)


def create_player(db, data):
    query = "INSERT INTO players(name, profession, hp, attack_points) VALUES (:name, :profession, :hp, :attack_points)"
    player = db.execute(query, data)

    return get_player_by_id(db, player.lastrowid)


def get_player_by_id(db, player_id):
    query = "SELECT rowid, name, profession, hp, attack_points, status, deaths, kills FROM players WHERE rowid =:id"
    params = {"id": player_id, }
    player = db.execute(query, params).fetchone()

    if not player:
        return None
    return player_to_dict(*player)

