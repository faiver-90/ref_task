import pytest
from httpx import AsyncClient
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.asyncio


@pytest.fixture
def test_user_data():
    return {
        "user_name": "test_user",
        "password": "test_password",
        "role": "user",
        "email": "test@example.com"
    }


@pytest.fixture
def test_updated_user_data():
    return {
        "user_name": "test_user",
        "email": "updated@example.com"
    }


@pytest.fixture
def test_admin_credentials():
    return {"username": "admin", "password": "1234"}


@pytest.fixture
def test_login_data(test_user_data):
    return {
        "username": test_user_data["user_name"],
        "password": test_user_data["password"]
    }


async def test_create_user(async_client: AsyncClient, test_user_data):
    response = await async_client.post("/users/create_user/", json=test_user_data)
    assert response.status_code == 200
    assert response.json()["detail"] == "User created"


async def test_login_user(async_client: AsyncClient, test_login_data):
    response = await async_client.post("/auth/token/", json=test_login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


async def test_get_user_by_token(async_client: AsyncClient, test_login_data):
    login_response = await async_client.post("/auth/token/", json=test_login_data)
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.get("/users/get_user_by_token/", headers=headers)
    assert response.status_code == 200
    assert "user_name" in response.json()


async def test_update_user(async_client: AsyncClient, test_login_data, test_updated_user_data):
    login_response = await async_client.post("/auth/token/", json=test_login_data)
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.put("/users/update_user/", headers=headers, json=test_updated_user_data)
    assert response.status_code == 200
    assert response.json()["detail"] == "User update"


async def test_delete_user(async_client: AsyncClient, test_login_data):
    login_response = await async_client.post("/auth/token/", json=test_login_data)
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.delete("/users/delete_user/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted"
