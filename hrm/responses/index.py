from . import *

@hr_app.get('/')
def index():
    return JSONResponse({'Message': "Working fine"}, status_code=status.HTTP_200_OK)