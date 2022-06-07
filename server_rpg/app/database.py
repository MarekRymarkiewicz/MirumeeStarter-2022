import sqlite3
import os
from contextlib import contextmanager

path = os.path.dirname(__file__)
db = os.path.join(path, 'example.db')


@contextmanager
def connection():
    conn = sqlite3.connect(db)
    try:
        yield conn
    except Exception:
        conn.rollback()
    finally:
        conn.close()


@contextmanager
def cursor():
    with connection() as cur:
        try:
            yield cur
        finally:
            cur.commit()
            cur.close()
