import sqlite3

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from database import cursor
from utils import default_profession_parameters
from crud import get_players, get_player_by_name, create_player, get_player_by_id
from sqlite3 import IntegrityError
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

async def players(request):
    with cursor() as cur:
        results = get_players(cur)
    return JSONResponse(results)


async def player(request):
    name = request.query_params.get('name')

    if not name:
        raise HTTPException(status_code=400, detail="A query name is required.")

    with cursor() as cur:
        result = get_player_by_name(cur, name)

    if result:
        return JSONResponse(result)
    raise HTTPException(status_code=404, detail="Could not find a player with this given name.")


async def player_id(request):
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
    if not "name" in data or not "profession" in data:
        raise HTTPException(status_code=400, detail="You need to supply character's name and profession.")
    data = profession_parameters | data

    #TODO: Refactor this to look shorter and be more scaleble
    try:
        with cursor() as cur:
            new_player = create_player(cur, data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Character's name has to be unique.")
    return JSONResponse(new_player)


# Database overview
async def players_table(request):
    with cursor() as cur:
        results = get_players(cur)
    context = {"request": request, "players": results}
    return templates.TemplateResponse("index.html", context)


app = Starlette(
    debug=True,
    routes=[
        Route('/api/players', players, methods=['GET']),
        Route('/api/player', player, methods=['GET']),
        Route('/api/player_id', player_id, methods=['GET']),
        Route('/api/players_table', players_table, methods=['GET']),
        Route('/api/player_create', player_create, methods=['POST']),
])
