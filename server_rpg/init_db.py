from app.database import cursor


with cursor() as cur:
    cur.execute(
        '''
        CREATE TABLE players
        (
            name text UNIQUE NOT NULL,
            profession text NOT NULL,
            hp INTEGER,
            attack_points INTEGER,
            status text NOT NULL DEFAULT 'offline',
            kills INTEGER DEFAULT 0,
            deaths INTEGER DEFAULT 0,
            password text NOT NULL
        )
        '''
    )
