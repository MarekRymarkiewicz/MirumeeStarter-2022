class PlayerAlreadyExists(Exception):
    def __init__(self):
        self.message = "Player with given name already exists."
        super().__init__(self.message)


class PlayerDoesNotExist(Exception):
    def __init__(self, player_id=None):
        if player_id:
            self.message = "Player with id = {} does not exist.".format(player_id)
        else:
            self.message = "Given player does not exist."
        super().__init__(self.message)


class PlayerIsOffline(Exception):
    def __init__(self):
        self.message = "Requested player is currently offline."
        super().__init__(self.message)


class PlayerIsOnline(Exception):
    def __init__(self):
        self.message = "Requested player is currently online."
        super().__init__(self.message)


class PlayerIsDead(Exception):
    def __init__(self):
        self.message = "Requested player is currently offline."
        super().__init__(self.message)


class FieldAlreadySet(Exception):
    def __init__(self):
        self.message = "Requested player already has given status."
        super().__init__(self.message)


class InvalidToken(Exception):
    def __init__(self):
        self.message = "A valid token is required"
        super().__init__(self.message)
