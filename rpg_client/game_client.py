import requests

class GameClient:
    def __init__(self):
        self.host_address = "http://127.0.0.1:8000/api/"
        self.commands = {
            "players": {"function": self.get_player_list,
                        "arguments": []},
            "online": {"function": self.make_character_online,
                       "arguments": ["player_id"]},
            "offline": {"function": self.make_character_offline,
                        "arguments": ["player_id"]},
            "login": {"function": self.login_character,
                      "arguments": ["character_name", "password"]},
            "attack": {"function": self.attack_character,
                       "arguments": ["player_id", "target_id", "token"]},
        }

    def send_get_request(self, endpoint, json={}):
        response = requests.get('{}{}'.format(self.host_address, endpoint), json=json)
        return response

    def send_post_request(self, endpoint, json={}):
        response = requests.post('{}{}'.format(self.host_address, endpoint), json=json)
        return response

    def get_player_list(self):
        response = self.send_get_request('players')
        return response

    def make_character_online(self, player_id):
        response = self.send_post_request('player/{}/online'.format(player_id))
        return response

    def make_character_offline(self, player_id):
        response = self.send_post_request('player/{}/offline'.format(player_id))
        return response

    def login_character(self, character_name, password):
        response = self.send_post_request('login', {"character_name": character_name, "password": password})
        return response

    def attack_character(self, player_id, target_id, token):
        response = self.send_post_request('player/{}/attack'.format(player_id), {"enemy_player_id": target_id,
                                                                                 "token": token})
        return response

    def execute(self, args: dict):
        try:
            command = self.commands[args["command"]]
            function = command["function"]
            required_arguments = command["arguments"]
            arguments = []
            for argument in required_arguments:
                arguments.append(args.get(argument))
            response = function(*arguments)
        except KeyError:
            return "Invalid command provided."
        except ValueError:
            return "Invalid argument value provided."
        except TypeError:
            return "You need an argument dictionary to execute."
        if response.status_code != 200:
            return response.text
        else:
            return response.json()
