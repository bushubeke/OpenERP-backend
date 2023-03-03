from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from sqladmin import Admin
from main.db import asyncengine
from users.responses import useradmin
from hrm.responses import hr_app
from users.admin import UserAdmin, RoleAdmin, RouteResponseAdmin


def create_dev_app():
    app = FastAPI(title="OpenERP Development App", version="0.0.1", debug=False)
    app.include_router(useradmin, prefix="/useradmin")
    app.include_router(hr_app, prefix="/hrm")
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    tok_bear = OAuth2PasswordBearer(tokenUrl="/auth/login")

    admin = Admin(app, asyncengine, title="Privelge Admin Dashboard")

    @app.get("/")
    def index():
        return {"Message": "Working"}

    add_pagination(app)
    admin.add_view(UserAdmin)
    admin.add_view(RoleAdmin)
    admin.add_view(RouteResponseAdmin)

    return app


def create_testing_app():
    app = FastAPI()
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def index():
        return {"Message": "You should make your own index page"}
