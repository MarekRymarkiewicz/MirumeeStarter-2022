import requests
from pprint import pprint
import argparse
from game_client import GameClient

parser = argparse.ArgumentParser()
# client = GameClient()
#
# if command == 'login':
#     client.login(player_id)

parser.add_argument("command", nargs="?")
parser.add_argument("--character-name", type=str)
parser.add_argument("--password", type=str)

args = parser.parse_args()
commands = {"login":{
                "character_name": args.character_name,
                "password": args.password
            },
            "attack":{
                "player_id": args.player_id,
                "password": args.password
            }
           }
args_json = {"character_name": args.character_name,
             "password": args.password
            }
#TODO: instead of makeclientonline/offline, create a class GameClient(): (has to handle connecting, handling exceptions, maing requests, making online/offline and attacking)

response = requests.post('http://127.0.0.1:8000/api/{}'.format(args.command), json=args_json)
print(response.json())
