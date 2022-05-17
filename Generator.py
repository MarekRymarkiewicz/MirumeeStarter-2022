import random


class Character:
    hp = 20
    mp = 0

    def __init__(self, name):
        self.name = name
        self.move_sequence = self.moves()

    def moves(self):
        while True:
            yield "attack", random.randint(0,5), 0
            yield "attack", random.randint(0,5), 0
            yield "super attack", random.randint(2,10), 0

    def move(self, target):
        move_type, move_power, move_cost = next(self.move_sequence)
        self.mp -= move_cost

        target.hp -= move_power
        print(f"{self.name} attacked {target.name} for {move_power} with {move_type}")
        if target.hp <= 0:
            print(f"{target.name} has died!")

    @property
    def is_alive(self):
        return self.hp > 0


class Mage(Character):
    hp = 20
    mp = 5

    def __init__(self, name):
        super().__init__(name)

    def moves(self):
        while True:
            if self.mp >= 5:
                yield "Fireball", random.randint(10,20), 5
            else:
                yield "attack", random.randint(0,5), 0
            self.mp += 1


class Warrior(Character):
    hp = 40
    mp = 0

    def __init__(self, name):
        super().__init__(name)


char1 = Warrior("Warrior")
char2 = Mage("Mage")

while char1.is_alive and char2.is_alive:
    # Roll initiative
    char1_initiative = random.randint(0,100)
    char2_initiative = random.randint(0,100)
    if char1_initiative > char2_initiative:
        char1.move(char2)
        if char2.is_alive:
            char2.move(char1)
    elif char1_initiative < char2_initiative:
        char2.move(char1)
        if char1.is_alive:
            char1.move(char2)
    else:
        pass
