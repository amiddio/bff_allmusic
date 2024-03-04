import pytest

from starlette import status

from .fixtures.user import *
from services.user import UserService


@pytest.mark.asyncio
async def test_user_register_negative_passwords_not_match(client: AsyncClient):
    input_data = {
        "email": "tester.testerovich@home.com",
        "name": "Tester Testerovich",
        "password": "qwerty",
        "password_repeat": "qwerty2"
    }
    response = await client.post("/users/register", json=input_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_user_register(client: AsyncClient):
    email = "tester.testerovich@home.com"
    input_data = {
        "email": email,
        "name": "Tester Testerovich",
        "password": "qwerty",
        "password_repeat": "qwerty"
    }
    response = await client.post("/users/register", json=input_data)
    assert response.status_code == status.HTTP_201_CREATED
    user = await UserService().get_user_by_email(email=email)
    assert user.email == email


@pytest.mark.asyncio
async def test_user_register_negative_exist(client: AsyncClient):
    input_data = {
        "email": "tester.testerovich@home.com",
        "name": "Tester Testerovich",
        "password": "qwerty",
        "password_repeat": "qwerty"
    }
    response = await client.post("/users/register", json=input_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_login_user(login, client: AsyncClient):
    assert login.status_code == status.HTTP_200_OK
    data = login.json()
    assert data.get('access_token') is not None
    assert data.get('token_type') == 'Bearer'


@pytest.mark.asyncio
async def test_login_user_negative_user(client: AsyncClient):
    input_data = {
        "username": "tester.testerovich111@home.com",
        "password": "qwerty"
    }
    response = await client.post("/users/login", data=input_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_user_negative_password(client: AsyncClient):
    input_data = {
        "username": "tester.testerovich@home.com",
        "password": "qwerty111"
    }
    response = await client.post("/users/login", data=input_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_user_detail(login, client: AsyncClient):
    data = login.json()
    headers = {
        'Authorization': f"{data.get('token_type')} {data.get('access_token')}"
    }
    response = await client.get("/users/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data.get('email') == 'tester.testerovich@home.com'


@pytest.mark.asyncio
async def test_check_user_permission_negative(login, client: AsyncClient):
    data = login.json()
    headers = {
        'Authorization': f"{data.get('token_type')} {data.get('access_token')}"
    }
    response = await client.get("/users/is_permission/1", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_subscribe_user_to_artists(login, client: AsyncClient):
    data = login.json()
    headers = {
        'Authorization': f"{data.get('token_type')} {data.get('access_token')}"
    }
    input_data = {
        "artist_ids": [3, 1, 2],
        "days": 30
    }
    response = await client.post("/subscribe", json=input_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_check_user_permission_again(login, client: AsyncClient):
    data = login.json()
    headers = {
        'Authorization': f"{data.get('token_type')} {data.get('access_token')}"
    }
    response = await client.get("/users/is_permission/1", headers=headers)
    assert response.status_code == status.HTTP_200_OK
