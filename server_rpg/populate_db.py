from app.database import cursor


# Name
# ClassName
# HP
# attack_point
# status_text
# kills
# deaths


with cursor() as cur:
    cur.execute(
        '''
        INSERT INTO players (name, profession, hp, attack_point) VALUES ('Siegfrid','Warrior',40,8)
        '''
    )

    cur.execute(
        '''
        INSERT INTO players (name, profession, hp, attack_point) VALUES ('Gandalf','Mage',20,18)
        '''
    )

    cur.execute(
        '''
        INSERT INTO players (name, profession, hp, attack_point) VALUES ('Elise','Rouge',25,16)
        '''
    )