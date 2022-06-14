def player_to_dict(id, name, profession, hp, attack_points, status, kills, deaths):
    return {"id": id,
            "name": name,
            "profession": profession,
            "hp": hp,
            "attack_point": attack_points,
            "status": status,
            "deaths": deaths,
            "kills": kills}


def default_profession_parameters(profession):
    profession_dict = {
                   "mage": {
                        "attack_points": 18,
                        "hp": 20
                   },
                   "warrior": {
                        "attack_points": 8,
                        "hp": 40
                   },
                   "rogue": {
                        "attack_points": 16,
                        "hp": 25
                   }
    }
    try:
        return profession_dict[profession]
    except KeyError:
        return {"attack_points": 8, "hp": 40}
