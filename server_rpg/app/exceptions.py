class PlayerAlreadyExists(Exception):
    def __init__(self):
        self.message = "Player with given name already exists."
        super().__init__(self.message)


class PlayerDoesNotExist(Exception):
    def __init__(self):
        self.message = "Searched player does not exist."
        super().__init__(self.message)


class PlayerIsOffline(Exception):
    def __init__(self):
        self.message = "Requested player is currently offline."
        super().__init__(self.message)


class PlayerIsDead(Exception):
    def __init__(self):
        self.message = "Requested player is currently offline."
        super().__init__(self.message)
