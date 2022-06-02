from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse


async def hello(request):
    return JSONResponse({"message": "Hello"})

app = Starlette(routes=[
    Route('/api/hello', hello, methods=['GET'])
])
