from app.database import cursor


# Name
# ClassName
# HP
# attack_point
# status_text
# kills
# deaths


with cursor() as cur:
    # Password: strength
    cur.execute(
        '''
        INSERT INTO 
        players (name, profession, hp, attack_points, password) 
        VALUES ('Siegfrid','Warrior',40,8,'e6b88623f7209b6c11fc49805c68752941074f4bc5eddd8c33bcdffc5419420d')
        '''
    )
    # Password: wisdom
    cur.execute(
        '''
        INSERT INTO 
        players (name, profession, hp, attack_points, password) 
        VALUES ('Gandalf','Mage',20,18,'7c68b70cea5555e5419f4bf32b38a9b7700a2c7e1d466d644878afcd48a867ec')
        '''
    )
    # Password: dexterity
    cur.execute(
        '''
        INSERT INTO 
        players (name, profession, hp, attack_points, password) 
        VALUES ('Elise','Rogue',25,16,'68f59df4675995f6f7cf66b7e140891ca269bc6a9b6a8fc08cb84085c9f3e8aa')
        '''
    )
