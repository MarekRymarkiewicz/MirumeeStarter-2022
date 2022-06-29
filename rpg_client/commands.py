import argparse
from game_client import GameClient

parser = argparse.ArgumentParser()
client = GameClient()

parser.add_argument("command", nargs="?")
parser.add_argument("--character-name")
parser.add_argument("--password")
parser.add_argument("--player-id")
parser.add_argument("--target-id")
parser.add_argument("--token")

args = parser.parse_args()

#TODO: instead of makeclientonline/offline, create a class GameClient(): (has to handle connecting, handling exceptions, maing requests, making online/offline and attacking)

print(client.execute(vars(args)))
