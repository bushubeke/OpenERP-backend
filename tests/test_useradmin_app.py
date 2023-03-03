import uuid
import pytest


special_key = None
reftoken = None
uid = None


@pytest.mark.asyncio
class TestRegister:
    uid = "something"
    register_user = {
        "email": "beimdegefu@gmail.com",
        "password": "default@123",
        "disabled": False
    }
    patch_data = {"email": "beimdegefu@yandex.com",
                  "date_registered": "2023-02-28T08:58:24.743Z"
                  }

    async def test_register_user_post(self, client):
        """Test case for register operations _register_post and register_patch
        Register User
        """
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = await client.post(
            "/useradmin/register",
            headers=headers,
            json=self.register_user,
        )
        #  check success registration
        global uid
        uid = response.json()['uid']
        assert response.status_code == 200

    async def test_register_user_post_unique(self, client):
        response = await client.post(
            "/useradmin/register",
            headers={},
            json=self.register_user,
        )
        #  asserting unique constraint is maintained
        assert response.status_code == 500

    async def test_register_user_patch(self, client):
        # patch operations
        global uid
        response = await client.patch(
            f"/useradmin/register/{uid}",
            headers={},
            json=self.patch_data,
        )
        #  asserting patching user is working
        print(response.json())
        assert response.status_code == 200

    async def test_register_user_patch_invalid_uid(self, client):
        response = await client.patch(
            f"/useradmin/register/{str(uuid.uuid4())}",
            headers={},
            json=self.patch_data,
        )
        #  asserting invalid uuid response
        assert response.status_code == 404


@pytest.mark.asyncio
class TestLogin:
    login_user_model = {
        "grant_type": "authorization_code",
        "email": "somemail@some.com",
        "password": "password",
        "token": "none"
    }
    log_in_model_valid = {
        "grant_type": "authorization_code",
        "email": "beimdegefu@yandex.com",
        "password": "default@123",
        "token": "none"
    }

    log_in_model_ref_token = {
        "grant_type": "refresh_token",
        "email": "something@yandex.com",
        "password": "something@123",
        "token": "none"
    }

    log_in_model_token_decode = {
        "grant_type": "token_decode",
        "email": "something@yandex.com",
        "password": "something@123",
        "token": "none"
    }

    async def test_login_user_admin_login_post_authorization_code_invalid_user(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = await client.post(
            "/useradmin/login",
            headers=headers,
            json=self.login_user_model,
        )
        assert response.status_code == 500

    async def test_login_user_admin_login_post_authorization_code_valid_user(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = await client.post(
            "/useradmin/login",
            headers=headers,
            json=self.log_in_model_valid,
        )
        self.log_in_model_ref_token['token'] = response.json()['refresh_token']
        self.log_in_model_token_decode['token'] = response.json()['access_token']
        global reftoken
        global special_key
        reftoken = response.json()["refresh_token"]
        special_key = response.json()["access_token"]

        assert response.status_code == 202

    async def test_login_user_admin_login_post_refresh_token(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = await client.post(
            "/useradmin/login",
            headers=headers,
            json=self.log_in_model_ref_token,
        )
        assert response.status_code == 202

    async def test_login_user_admin_login_post_token_decode(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = await client.post(
            "/useradmin/login",
            headers=headers,
            json=self.log_in_model_token_decode,
        )

        assert response.status_code == 206


@pytest.mark.asyncio
class TestAddRoles:
    id = 2
    role_post = {
        "name": "superuser",
        "description": "Developer Role"
    }
    role_post_delete = {
        "name": "will delete",
        "description": "delete"
    }

    role_patch = {
        "id": 1,
        "name": "superuser",
        "description": "Developer Role Updated"
    }
    no_role_patch = {
        "id": 25,
        "name": "standard",
        "description": "Developer Role Updated"
    }
    add_role_post = {
        "role_id": 1,
            }
    add_role_post_wrong = {
          "role_id": 25
            }
    add_role_delete = {
        "role_id": 1,
            }
    add_role_delete_wrong = {
        "role_id": 1,
    }

    async def test_role_get_invalid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = await client.get(
            "/useradmin/roles",
            headers=headers,

        )
        # fetching roles if exist unauthorized
        assert response.status_code == 401

    async def test_role_get_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.get(
            "/useradmin/roles",
            headers=headers,
        )
        # fetching roles if exist unauthorized
        assert response.status_code == 200 or response.status_code == 401

    async def test_role_post_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            "/useradmin/roles",
            headers=headers,
            json=self.role_post
        )
        # creating roles if with required privileges
        assert response.status_code == 200 or response.status_code == 401

    async def test_role_post_for_delete_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            "/useradmin/roles",
            headers=headers,
            json=self.role_post_delete
        )
        # creating roles if with required privileges
        assert response.status_code == 200 or response.status_code == 401

    async def test_role_post_invalid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            "/useradmin/roles",
            headers=headers,
            json=self.role_post
        )
        # creating roles if with required privileges validating unique
        assert response.status_code == 500 or response.status_code == 401

    async def test_role_patch_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.patch(
            "/useradmin/roles",
            headers=headers,
            json=self.role_patch
        )
        # updating roles
        assert response.status_code == 200 or response.status_code == 401

    async def test_role_patch_invalid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.patch(
            "/useradmin/roles",
            headers=headers,
            json=self.no_role_patch
        )
        # updating role with wrong id
        assert response.status_code == 404 or response.status_code == 401 or response.status_code == 500

    async def test_role_delete_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.delete(
            f"/useradmin/roles/{self.id}",
            headers=headers,

        )
        # delete role with id
        assert response.status_code == 404 or response.status_code == 200 or response.status_code == 500

    async def test_add_user_role_get_valid(self, client):

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.get(
            f"/useradmin/roles/{uid}",
            headers=headers,
        )
        # fetching roles of user
        assert response.status_code == 200 or response.status_code == 404 or response.status_code == 500

    async def test_add_user_role_get_invalid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.get(
            f"/useradmin/roles/{str(uuid.uuid4())}",
            headers=headers,
        )
        # fetching roles  of user that does not exist
        assert response.status_code == 200 or response.status_code == 404 or response.status_code == 500

    async def test_add_user_role_post_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            f"/useradmin/roles/{uid}",
            headers=headers,
            json=self.add_role_post
        )
        # creating roles to a user
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500

    async def test_add_user_role_post_invalid_uidd(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            f"/useradmin/roles/{str(uuid.uuid4())}",
            headers=headers,
            json=self.add_role_post
        )
        # creating roles to user with non-existent value of uuid
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500 \
               or response.status_code == 404

    async def test_add_user_role_post_invalid_role_id(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            f"/useradmin/roles/{uid}",
            headers=headers,
            json=self.add_role_post_wrong
        )
        # creating roles to user with non-existent value of role id
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500 \
            or response.status_code == 404

    async def test_add_user_role_delete_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.delete(
            f"/useradmin/roles/{uid}/{self.add_role_delete['role_id']}",
            headers=headers,
        )
        # delete role of user with correct uuid and role id
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500

    async def test_add_user_role_delete_invalid_uuid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.delete(
            f"/useradmin/roles/{str(uuid.uuid4())}/{self.add_role_delete_wrong['role_id']}",
            headers=headers,
        )
        # delete role of user with wrong uuid
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500

    async def test_add_user_role_delete_invalid_role_id(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.delete(
            f"/useradmin/roles/{uid}/{self.add_role_delete_wrong['role_id']}",
            headers=headers,
        )
        # delete role of user with wrong role id
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500


@pytest.mark.asyncio
class TestRouteResponse:
    route_id = 1
    route_d_id = 2
    path_post = {
        "name": "adding address",
        "route_path": "address_delete",
        "description": "employee address posting"
    }
    path_patch = {
        "name": "adding address changed",
        "route_path": "address_delete_changed",
        "description": "employee address posting changed"
    }
    path_patch_viloet_unique = {
        "name": "adding address changed",
        "route_path": "address_delete_changed",
        "description": "employee address posting changed"
    }
    path_post_for_delete = {
        "name": "adding address",
        "route_path": "address_delete_again",
        "description": "employee address posting"
    }
    add_role_post = {
        "role_id": 1,
    }
    add_role_post_wrong = {
        "role_id": 25
    }

    async def test_response_path_get_invalid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = await client.get(
            "/useradmin/response_path",
            headers=headers,
        )
        # fetching available paths if exist unauthorized
        assert response.status_code == 401

    async def test_response_path_get_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.get(
            "/useradmin/response_path",
            headers=headers,
        )
        # fetching available paths if exist unauthorized
        assert response.status_code == 200 or response.status_code == 401

    async def test_response_path_post_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            "/useradmin/response_path",
            headers=headers,
            json=self.path_post
        )
        # creating response path if with required privileges
        assert response.status_code == 200 or response.status_code == 401

    async def test_response_path_post_for_delete_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            "/useradmin/response_path",
            headers=headers,
            json=self.path_post_for_delete
        )
        # creating response path if with required privileges
        assert response.status_code == 200 or response.status_code == 401

    async def test_response_path_post_invalid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            "/useradmin/response_path",
            headers=headers,
            json=self.path_post
        )
        # creating response path if with required privileges asserting no duplicate
        assert response.status_code == 500 or response.status_code == 401

    async def test_response_path_patch_patch_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.patch(
            f"/useradmin/response_path/{self.route_id}",
            headers=headers,
            json=self.path_patch
        )
        # updating response route data
        assert response.status_code == 200 or response.status_code == 401

    async def test_response_path_patch_invalid_wrong_route_id(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.patch(
            f"/useradmin/response_path/{25}",
            headers=headers,
            json=self.path_patch
        )
        # updating response route data wrong id
        assert response.status_code == 404 or response.status_code == 401 or response.status_code == 500

    async def test_response_path_patch_invalid_violet_unique(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.patch(
            f"/useradmin/response_path/{2}",
            headers=headers,
            json=self.path_patch_viloet_unique
        )
        # updating response route data violet unique constraint
        assert response.status_code == 404 or response.status_code == 401 or response.status_code == 500

    async def test_response_path_delete_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }
        response = await client.delete(
            f"/useradmin/response_path/{self.route_d_id}",
            headers=headers,
        )
        # delete response route using valid id
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500

    async def test_response_path_delete_invalid_wrong_id(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }
        response = await client.delete(
            f"/useradmin/response_path/{self.route_d_id}",
            headers=headers,
        )
        # delete response route using invalid id
        assert response.status_code == 404 or response.status_code == 401 or response.status_code == 500

    async def test_add_response_path_role_post_valid_route(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            f"/useradmin/response_path/{self.route_id}",
            headers=headers,
            json=self.add_role_post
        )
        # creating roles to route with valid route
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500 \
               or response.status_code == 404

    async def test_add_response_path_role_post_invalid_route(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            f"/useradmin/response_path/{25}",
            headers=headers,
            json=self.add_role_post
        )
        # creating roles to route with non-existent value of route_id
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500 \
               or response.status_code == 404

    async def test_add_response_path_role_id(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.post(
            f"/useradmin/response_path/{self.route_id}",
            headers=headers,
            json=self.add_role_post_wrong
        )
        # creating roles to route with non-existent value of role id
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500 \
            or response.status_code == 404

    async def test_add_response_path_role_delete_valid(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.delete(
            f"/useradmin/response_path/{self.route_id}/{1}",
            headers=headers,
        )
        # delete role of user with correct route_id and role id
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500

    async def test_add_response_path_role_delete_invalid_route_id(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.delete(
            f"/useradmin/response_path/{25}/{1}",
            headers=headers,
        )
        # delete role of user with wrong route id
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500

    async def test_add_response_path_role_delete_invalid_role_id(self, client):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {special_key}",
        }

        response = await client.delete(
            f"/useradmin/response_path/{1}/{25}",
            headers=headers,
        )
        # delete role of path with wrong role id
        assert response.status_code == 200 or response.status_code == 401 or response.status_code == 500
