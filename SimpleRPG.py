import random


class Weapon:
    name = None
    damage = 5
    accuracy = 100
    damage_deviation = 0.0

    def __init__(self, name, damage, accuracy, damage_deviation=0.0):
        self.name = name
        self.damage = damage
        self.accuracy = accuracy
        self.damage_deviation = damage_deviation

    def roll_damage(self):
        return round(self.damage * random.uniform(1.0 - self.damage_deviation, (1.0 + self.damage_deviation)))


weapon_dict = {
    "fists": Weapon("fists", 3, 100),
    "spear": Weapon("spear", 8, 110, 0.2),
    "bow": Weapon("bow", 7, 95, 0.3),
    "fireball": Weapon("fireball", 18, 80, 0.6)
}


class Character:
    max_hp = 100
    hp = 100
    mp = 0
    dodge_value = 0
    armour_value = 0
    weapon = weapon_dict["fists"]

    def __init__(self, name):
        self.name = name

    def is_alive(self):
        return self.hp > 0

    def strike(self, target):
        # Check if attack hits
        if random.randint(0, self.weapon.accuracy) < target.dodge_value:
            print(f"{self.name} missed {target.name}!")
            return
        else:
            # Deal damage if hit
            damage = self.weapon.roll_damage() - target.armour_value
            target.hp -= damage
            print(f"{self.name} strikes {target.name} with {self.weapon.name} for {damage} HP!")
            if target.hp <= 0:
                print(f"{target.name} has died!")


class Mage(Character):
    max_hp = 80
    hp = max_hp
    mp = 50
    dodge_value = 10
    armour_value = 0
    weapon = weapon_dict["fireball"]

    def __init__(self, name):
        super().__init__(name)


class Warrior(Character):
    max_hp = 100
    hp = max_hp
    mp = 0
    dodge_value = 0
    armour_value = 4
    weapon = weapon_dict["spear"]

    def __init__(self, name):
        super().__init__(name)


class Rogue(Character):
    max_hp = 90
    hp = max_hp
    mp = 50
    dodge_value = 50
    armour_value = 2
    weapon = weapon_dict["bow"]

    def __init__(self, name):
        super().__init__(name)


char1 = Warrior("Warrior")
char2 = Rogue("Rogue")

while char1.is_alive() and char2.is_alive():
    # Roll initiative
    char1_initiative = random.randint(0,100)
    char2_initiative = random.randint(0,100)
    if char1_initiative > char2_initiative:
        char1.strike(char2)
        if char2.is_alive():
            char2.strike(char1)
    elif char1_initiative < char2_initiative:
        char2.strike(char1)
        if char1.is_alive():
            char1.strike(char2)
    else:
        pass
