from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from database import cursor
from crud import get_players

from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

async def players(request):
    with cursor() as cur:
        results = get_players(cur)
    return JSONResponse(results)


async def players_table(request):
    with cursor() as cur:
        results = get_players(cur)
    context = {"request": request, "players": results}
    return templates.TemplateResponse("index.html", context)


app = Starlette(routes=[
    Route('/api/players', players, methods=['GET']),
    Route('/api/players_table', players_table, methods=['GET'])
])
