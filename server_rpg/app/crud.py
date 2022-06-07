from database import cursor


def get_players(db):
    results = []
    query = "SELECT rowid, name, profession, hp, attack_point, status, deaths, kills FROM players"

    for player in db.execute(query):
        player_data = player

        # TODO: [[1, Damian],[2,Tomek]]
        # Change code so the result's data structure looks like this:
        # [{"id": 1, name: "Damian"},{"id": 1, name: "Damian"}]

        results.append(player_data)

    return results


# def get_players():
#     players = []
#     with cursor() as cur:
#         query = cur.execute("SELECT * FROM players")
#         result = query.fetchall()
#         for row in result:
#             players.append(row)
#     return players
