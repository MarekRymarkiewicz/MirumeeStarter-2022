def player_to_dict(id, name, profession, hp, attack_points, status, kills, deaths):
    return {"id": id,
            "name": name,
            "profession": profession,
            "hp": hp,
            "attack_point": attack_points,
            "status": status,
            "deaths": deaths,
            "kills": kills}
