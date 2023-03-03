import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, DateTime, Column, Integer, Float, String, ForeignKey, UniqueConstraint
# from sqlalchemy.dialects.postgresql import UUID
from main.db import Base
from hrm.models import  Employee

# import enum
# from sqlalchemy import Enum

# class MyEnum(enum.Enum):
#     one = 1
#     two = 2
#     three = 3

# t = Table(
#     'data', MetaData(),
#     Column('value', Enum(MyEnum))
# )


class Role(Base):
    __tablename__ = 'admin_role'
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    name = Column(String(80), unique=True)
    description = Column(String(255))
    users = relationship("User", secondary='admin_roles_users', back_populates="roles", lazy="selectin")
    pages = relationship('RouteResponse', secondary='admin_roles_route_response', back_populates='roles')

    def __str__(self):
        return f"{self.name}"


class User(Base):
    """ User Model for storing user related details """
    __tablename__ = "admin_user"
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    uid = Column(String(36), unique=True, default=str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(500), nullable=False)
    date_registered = Column(DateTime(timezone=True), default=func.now())
    disabled = Column(Boolean(), default=True)
    roles = relationship('Role', secondary='admin_roles_users', back_populates="users", lazy='joined')
    name = relationship(Employee, back_populates='users')
def __str__(self):
        return f"{self.email}"


class RolesUsers(Base):
    __tablename__ = 'admin_roles_users'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column('user_id', Integer(), ForeignKey('admin_user.id', ondelete="CASCADE"), nullable=False)
    role_id = Column('role_id', Integer(), ForeignKey('admin_role.id', ondelete="CASCADE"), nullable=False)
    UniqueConstraint(user_id, role_id)

    def __str__(self):
        return f"<UserRole '{self.id}'>"


class RouteResponse(Base):
    __tablename__ = 'admin_route_response'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=True)
    route_path = Column(String(300), unique=True, nullable=False)
    description = Column(String(255))
    roles = relationship('Role', secondary='admin_roles_route_response', back_populates='pages')

    def __str__(self):
        return f"{self.name}"


class RouteResponseRoles(Base):
    __tablename__ = 'admin_roles_route_response'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    route_id = Column('page_id', Integer(), ForeignKey('admin_route_response.id', ondelete="CASCADE"), nullable=False)
    role_id = Column('role_id', Integer(), ForeignKey('admin_role.id', ondelete="CASCADE"), nullable=False)
    UniqueConstraint(route_id, role_id)

    def __str__(self):
        return f"PageRoles '{self.id}'"


class SiteData(Base):
    __tablename__ = 'admin_site_data'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    remote_add = Column(String(50), nullable=False)
    accessed_route = Column(String(1000), nullable=False)
    method = Column(String(7), nullable=False)
    response_time = Column(Float(), nullable=True)
    response_status = Column(String(80), nullable=True)

    def __str__(self):
        return f"{self.remote_add}-{self.accessed_route}"
