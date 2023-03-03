import os
import jwt
import uuid
from uuid import uuid4, UUID
from random import randint
from typing import Any
from datetime import datetime, timedelta
from fastapi_pagination import Page, paginate
from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select, update, delete, exists, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, subqueryload, selectinload
from passlib.hash import pbkdf2_sha512
from main.db import get_session
from users.models import User, RolesUsers, RouteResponse, RouteResponseRoles, Role, SiteData
from users.serializers import RoleModel, UserModel, UserModelAll, RolesUsersModel, \
    RoleModelMatrix, UserModelLogin, RoleModelAll, LoginUserModel, RoleUserModelAll, AddRole, \
    RoutesRolesModel, RouteResponseModel, RouteResponsePostModel, \
    RouteResponseDeleteModel, UserModelUpdate, UserModelPost
from config import settings
from erplogging import logger


useradmin = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="useradmin/token")

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    key = settings.SECRET_KEY
    data = jwt.decode(token, key, algorithms="HS256")
    user = data["data"]

    # print(f"{request.scope['route'].name}")
    # print(f"{str(request.url_for('get_one_user',user_id=1)).replace(str(request.base_url),'/')}")
    # print(request.path_params)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

from users.responses.index import index
from users.responses.roles import role_post, role_patch, role_get, role_delete, add_user_role_get, \
    add_user_role_delete, add_user_role_post
from users.responses.userops import get_one_user
from users.responses.login import login_user, login_swagger
from users.responses.register import register,register_patch
from users.responses.userops import get_one_user, get_some_user
from users.responses.routepath import response_path_get, response_path_post, response_path_patch, \
    response_path_delete, add_response_path_role_delete, add_response_path_role_post

