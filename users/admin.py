from sqladmin import ModelView
from users.models import Role, User, RouteResponse


class UserAdmin(ModelView, model=User):
    column_list = ['id', 'email', 'password', 'date_registered', 'roles']
    column_searchable_list = ['email']
    column_default_sort = 'id'
    column_sortable_list = ['id', 'email']
    can_create = True
    form_excluded_columns = [User.date_registered]


class RoleAdmin(ModelView, model=Role):
    column_list = ['id', 'name', 'description']
    column_sortable_list = ['id']
    column_default_sort = 'id'
    can_create = True


class RouteResponseAdmin(ModelView, model=RouteResponse):
    column_list = ['id', 'name', 'route_path', 'description', 'roles']
    column_searchable_list = ['name', 'route_path', 'description']
    column_default_sort = 'id'
    column_sortable_list = ['id', 'name']
    can_create = True
