from . import *


@useradmin.get('/')
async def index() -> Any:

    return JSONResponse({'Message': "Working fine"}, status_code=status.HTTP_200_OK)
