import uuid
from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, EmailStr, Field, validator
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from users.models import SiteData


SiteDataModel = sqlalchemy_to_pydantic(SiteData)


class RoleModel(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class RoleModelMatrix(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True

class UserModelPost(BaseModel):
    email: EmailStr
    password: str
    disabled: Optional[bool]


class UserModel(BaseModel):
    uid: uuid.UUID = None
    email: EmailStr
    password: str
    disabled: Optional[bool]

    @validator('uid', pre=True, always=True)
    def set_id(cls, v):
        return v or uuid.uuid4()

    class Config:
        orm_mode = True


class ContentTypesModel(BaseModel):
    model_name: str
    read_roles: List[RoleModelMatrix]
    write_roles: List[RoleModelMatrix]

    class Config:
        orm_mode = True


class LoginUserModel(BaseModel):
    grant_type: Literal['authorization_code', 'refresh_token', 'token_decode'] = "authorization_code"
    email: EmailStr
    password: str
    token: Optional[str] = 'none'


class RoleUserModelAll(BaseModel):
    id: Optional[int]
    roles: Optional[List[RoleModelMatrix]] = []

    class Config:
        orm_mode = True


class AddRole(BaseModel):
    role_id: int


class UserModelAll(BaseModel):
    id: Optional[int]
    uid: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    disabled: Optional[bool]
    date_registered: Optional[datetime]
    roles: Optional[List[RoleModelMatrix]] = []

    class Config:
        orm_mode = True


class UserModelUpdate(BaseModel):
    email: Optional[EmailStr]
    date_registered: Optional[datetime]


class RoleUserModel(BaseModel):
    id: Optional[int]
    uid: Optional[uuid.UUID]
    email: Optional[EmailStr]
    roles: Optional[List[RoleModelMatrix]] = []

    class Config:
        orm_mode = True


class UserNameModel(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserLoader(BaseModel):
    uid: Optional[uuid.UUID]
    name: List[UserNameModel]
    email: Optional[EmailStr]
    disabled: Optional[bool]
    roles: Optional[List[RoleModel]] = []
    is_active: bool
    is_authenticated: bool = False

    class Config:
        orm_mode = True


class RoleModelAll(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    users: Optional[List[UserModel]] = []

    class Config:
        orm_mode = True


class UserModelLogin(BaseModel):
    id: Optional[int]
    uid: Optional[uuid.UUID]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    roles: Optional[List[RoleModel]] = []


class RolesUsersModel(BaseModel):
    user_id: int
    role_id: int


class ContentRolesModel(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True


class RouteResponseModel(BaseModel):
    id: int
    name: str
    route_path: str
    description: str
    roles:  Optional[List[RoleModel]]

    class Config:
        orm_mode = True


class RouteResponsePostModel(BaseModel):
    name: str
    route_path: str
    description: str

    class Config:
        orm_mode = True


class RouteResponseDeleteModel(BaseModel):
    id: int
    name: str
    route_path: str
    description: str
    roles: Optional[List[RoleModel]]

    class Config:
        orm_mode = True


class RoutesRolesModel(BaseModel):
    route_id: int
    role_id: int

    class Config:
        orm_mode = True
