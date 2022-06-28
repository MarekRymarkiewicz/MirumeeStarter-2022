import jwt
from exceptions import InvalidToken
from functools import wraps
SECRET_KEY = "CustodianKey"
from hashlib import sha256


# Decorators
def require_token(fn):
    @wraps(fn)
    async def decorated_func(*args, **kwargs):
        request = args[0]
        data = await request.json()
        token = data["token"]
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return await fn(*args, **kwargs)
        except:
            raise
    return decorated_func


# Functions
def player_to_dict(id, name, profession, hp, attack_points, status, kills, deaths):
    return {"id": id,
            "name": name,
            "profession": profession,
            "hp": hp,
            "attack_points": attack_points,
            "status": status,
            "kills": kills,
            "deaths": deaths
            }


def default_profession_parameters(profession):
    profession = profession.lower()
    profession_dict = {
                   "mage": {
                        "attack_points": 18,
                        "hp": 20
                   },
                   "warrior": {
                        "attack_points": 8,
                        "hp": 40
                   },
                   "rogue": {
                        "attack_points": 16,
                        "hp": 25
                   },
    }
    try:
        return profession_dict[profession]
    except KeyError:
        return False


def sha256_encrypt(string_to_hash):
    encrypted_string = sha256(string_to_hash.encode()).hexdigest()
    return encrypted_string
