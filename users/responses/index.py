from . import *


@useradmin.get('/')
async def index(request: Request) -> Any:
    print([x.name for x in request.app.routes])
    return JSONResponse({'Message': "Working fine"}, status_code=status.HTTP_200_OK)
