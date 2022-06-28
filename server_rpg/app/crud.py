from utils import player_to_dict, default_profession_parameters, sha256_encrypt
from exceptions import PlayerAlreadyExists, PlayerDoesNotExist, PlayerIsOffline, PlayerIsDead, FieldAlreadySet


def get_players(db):
    results = []
    query = "SELECT rowid, name, profession, hp, attack_points, status, kills, deaths FROM players"

    for player in db.execute(query):
        player_data = player_to_dict(*player)
        results.append(player_data)

    return results


def get_player_by_name(db, player_name):
    query = "SELECT rowid, name, profession, hp, attack_points, status, kills, deaths FROM players WHERE name =:name COLLATE NOCASE"
    params = {"name": player_name, }
    player = db.execute(query, params).fetchone()

    if not player:
        raise PlayerDoesNotExist
    return player_to_dict(*player)


def create_player(db, data):
    try:
        player_name = get_player_by_name(db, data["name"])
    except PlayerDoesNotExist:
        data["password"] = sha256_encrypt(data["password"])
        query = "INSERT INTO players(name, profession, hp, attack_points, password) VALUES (:name, :profession, :hp, :attack_points, :password)"
        player = db.execute(query, data)

    return get_player_by_id(db, player.lastrowid)


def get_player_by_id(db, player_id):
    query = "SELECT rowid, name, profession, hp, attack_points, status, kills, deaths FROM players WHERE rowid =:id"
    params = {"id": player_id, }
    player = db.execute(query, params).fetchone()

    if not player:
        raise PlayerDoesNotExist
    return player_to_dict(*player)


def set_player_status(db, player_id, status):
    if status != "offline" and status != "online":
        raise ValueError

    query = "UPDATE players SET status = :status WHERE rowid =:player_id"
    params = {"player_id": player_id, "status": status}
    player = get_player_by_id(db, player_id)
    if player["status"] == status:
        raise FieldAlreadySet
    db.execute(query, params)
    return get_player_by_id(db, player_id)


def get_player_hash(db, player_id):
    query = "SELECT password FROM players WHERE rowid =:player_id"
    params = {"player_id": player_id, }
    player = db.execute(query, params).fetchone()
    player_hash = player[0]
    return player_hash


def kill_player(db, player_id, target_id):
    player = get_player_by_id(db, player_id)
    target = get_player_by_id(db, target_id)
    query = "UPDATE players SET kills = kills + 1 WHERE rowid =:player_id"
    params = {"player_id": player_id, }
    db.execute(query, params)
    query = "UPDATE players SET hp = :hp, deaths = deaths + 1 WHERE rowid =:target_id"
    params = {"hp": default_profession_parameters(target['profession'])["hp"], "target_id": target_id}
    db.execute(query, params)

    target = set_player_status(db, target_id, "offline")
    player["kills"] += 1
    # TODO: Autoryzacja z JWT - JSON Web Talker
    result = [player, target]
    return result


def player_attack(db, player_id, target_id):
    query = "UPDATE players SET hp = :new_hp WHERE rowid =:target_id"

    player = get_player_by_id(db, player_id)
    target = get_player_by_id(db, target_id)

    # Check if both players are online
    if target["status"] == "offline" or player["status"] == "offline":
        raise PlayerIsOffline
    # Check if both players are alive
    if target["hp"] <= 0 or player["hp"] <= 0:
        raise PlayerIsDead

    target["hp"] -= player["attack_points"]

    if target["hp"] <= 0:
        result = kill_player(db, player_id, target_id)
    else:
        params = {"target_id": target_id, "new_hp": target["hp"], }
        db.execute(query, params)
        result = [player, target]
    return result
