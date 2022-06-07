from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from database import cursor
from crud import get_players


async def players(request):
    with cursor() as cur:
        results = get_players(cur)
    return JSONResponse(results)


app = Starlette(routes=[
    Route('/api/players', players, methods=['GET'])
])
