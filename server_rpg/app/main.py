import json
import jwt
import datetime
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, RedirectResponse
from starlette.requests import Request
from database import cursor
from utils import default_profession_parameters, SECRET_KEY, require_token, sha256_encrypt
from crud import get_players, get_player_by_name, create_player, get_player_by_id, set_player_status, player_attack, get_player_hash
from exceptions import PlayerAlreadyExists, PlayerDoesNotExist, PlayerIsOffline, PlayerIsDead, FieldAlreadySet
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles


templates = Jinja2Templates(directory='templates')


async def players(request):
    with cursor() as cur:
        results = get_players(cur)
    return JSONResponse(results)


async def get_player(request):
    data = await request.json()
    name = data['name']

    if not name:
        raise HTTPException(status_code=400, detail="A query name is required.")

    with cursor() as cur:
        result = get_player_by_name(cur, name)

    if result:
        return JSONResponse(result)
    raise HTTPException(status_code=404, detail="Could not find a player with this given name.")


async def get_player_id(request):
    data = await request.json()
    try:
        with cursor() as cur:
            result = get_player_by_id(cur, data["id"])
    except KeyError:
        raise HTTPException(status_code=400, detail="A query ID is required.")
    except ValueError:
        raise HTTPException(status_code=404, detail="Could not yield a result.")

    if result:
        return JSONResponse(result)
    raise HTTPException(status_code=404, detail="Could not find a player with this given ID.")


async def player_create(request):
    data = await request.json()
    profession_parameters = default_profession_parameters(data.get("profession"))
    if not "name" in data or not "profession" in data or not "password" in data:
        raise HTTPException(status_code=400, detail="You need to provide character's name, profession and password.")
    data = profession_parameters | data

    try:
        with cursor() as cur:
            new_player = create_player(cur, data)
    except PlayerAlreadyExists:
        raise HTTPException(status_code=409, detail="Character's name has to be unique.")
    return JSONResponse(new_player)


async def set_player_status_offline(request):
    with cursor() as cur:
        try:
            player = get_player_by_id(cur, request.path_params['player_id'])
        except PlayerDoesNotExist:
            raise HTTPException(status_code=404, detail="No character found.")
        try:
            player = set_player_status(cur, request.path_params['player_id'], "offline")
        except FieldAlreadySet:
            raise HTTPException(status_code=409, detail="Player is already offline.")
    return JSONResponse(player)


async def set_player_status_online(request):
    with cursor() as cur:
        try:
            player = get_player_by_id(cur, request.path_params['player_id'])
        except PlayerDoesNotExist:
            raise HTTPException(status_code=404, detail="No character found.")
        try:
            player = set_player_status(cur, request.path_params['player_id'], "online")
        except FieldAlreadySet:
            raise HTTPException(status_code=409, detail="Player is already online.")
    return JSONResponse(player)


@require_token
async def attack(request):
    try:
        data = await request.json()
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=409, detail="You need to send target's ID via JSON request.")

    player_id = request.path_params['player_id']
    try:
        target_id = data["enemy_player_id"]
        int(target_id)
    except KeyError:
        raise HTTPException(status_code=409, detail="You must provide target's ID.")
    except ValueError:
        raise HTTPException(status_code=409, detail="Target's ID has to be an integer.")

    if player_id == target_id:
        raise HTTPException(status_code=409, detail="Player cannot target himself.")

    with cursor() as cur:
        # Check if attacking character exists
        try:
            get_player_by_id(cur, request.path_params['player_id'])
        except PlayerDoesNotExist:
            raise HTTPException(status_code=404, detail="No player character found.")

        # Check if target character exists
        try:
            get_player_by_id(cur, data["enemy_player_id"])
        except PlayerDoesNotExist:
            raise HTTPException(status_code=404, detail="No target character found.")

        try:
            result = player_attack(cur, request.path_params['player_id'], data["enemy_player_id"])
        except PlayerIsOffline:
            raise HTTPException(status_code=409, detail="Both players have to be online.")
        except PlayerIsDead:
            raise HTTPException(status_code=409, detail="Both players have to be alive.")

    return JSONResponse(result)


async def login(request):
    form_data = await request.json()
    try:
        provided_credentials = {"character_name": form_data["character_name"], "password": form_data['password']}
    except KeyError:
        raise HTTPException(status_code=409, detail="You have to provide character's name and password.")
    with cursor() as cur:
        try:
            player_id = get_player_by_name(cur, provided_credentials["character_name"])["id"]
        except PlayerDoesNotExist:
            raise HTTPException(status_code=404, detail="No character with given name have been found.")
        player_hash = get_player_hash(cur, player_id)
    if sha256_encrypt(provided_credentials["password"]) != player_hash:
        raise HTTPException(status_code=401, detail="Provided invalid credentials.")

    token = jwt.encode(
        {"user": provided_credentials["character_name"],
         "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
        SECRET_KEY
        )
    # with cursor() as cur:
    #     set_player_status(cur, get_player_by_name(cur, provided_credentials["character_name"])["id"], "online")

    return JSONResponse({"token": token})


# Database overview
async def players_table(request):
    with cursor() as cur:
        results = get_players(cur)
    context = {"request": request, "players": results}
    return templates.TemplateResponse("index.html", context)


# User login form UI
async def login_form(request):
    context = {"request": request}
    state = request.query_params.get("state")
    if state == "invalid":
        context["state"] = state
    return templates.TemplateResponse("login.html", context)


async def login_form_data(request):
    form_data = await request.form()
    try:
        provided_credentials = {"character_name": form_data["character_name"], "password": form_data['password']}
    except KeyError:
        return RedirectResponse(url="login_form?state=invalid&status_code=409")
    with cursor() as cur:
        try:
            player_id = get_player_by_name(cur, provided_credentials["character_name"])["id"]
        except PlayerDoesNotExist:
            return RedirectResponse(url="login_form?state=invalid&status_code=404")
        player_hash = get_player_hash(cur, player_id)
    if sha256_encrypt(provided_credentials["password"]) != player_hash:
        return RedirectResponse(url="login_form?state=invalid&status_code=401")

    token = jwt.encode(
        {"user": provided_credentials["character_name"],
         "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
        SECRET_KEY
        )
    # with cursor() as cur:
    #     set_player_status(cur, get_player_by_name(cur, provided_credentials["character_name"])["id"], "online")

    return JSONResponse({"token": token})


app = Starlette(
    debug=True,
    routes=[
        Route('/api/players', players, methods=['GET']),
        Route('/api/player', get_player, methods=['GET']),
        Route('/api/player_id', get_player_id, methods=['GET']),
        Route('/api/player_create', player_create, methods=['POST']),
        Route('/api/player/{player_id:int}/offline', set_player_status_offline, methods=['POST']),
        Route('/api/player/{player_id:int}/online', set_player_status_online, methods=['POST']),
        Route('/api/player/{player_id:int}/attack', attack, methods=['POST']),
        Route('/api/login', login, methods=['POST']),
        # Jinja2 Template Responses
        Route('/api/players_table', players_table, methods=['GET']),
        Route('/api/login_form', login_form, methods=['GET', 'POST']),
        Route('/api/login_form_data', login_form_data, methods=['POST']),
        # Static file mounts
        Mount('/stylesheets', StaticFiles(directory='stylesheets'), name='stylesheets'),
        Mount('/scripts', StaticFiles(directory='scripts'), name='scripts'),
    ]
)

# issues:
# Self-harm,
# attacking offline players
# what happens when player dies
# holding current hp
