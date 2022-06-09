from starlette.applications import Starlette
from starlette.routing import Route
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from database import cursor
from crud import get_players, get_player_by_name

from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

async def players(request):
    with cursor() as cur:
        results = get_players(cur)
    return JSONResponse(results)


async def player(request):
    name = request.query_params.get('name')

    if not name:
        raise HTTPException(status_code=404, detail="A query name is required.")

    with cursor() as cur:
        result = get_player_by_name(cur, name)

    if result:
        return JSONResponse(result)
    raise HTTPException(status_code=404, detail="Could not find a player with this given name.")

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
        Route('/api/players_table', players_table, methods=['GET'])
])
