import asyncio

import pytest
from httpx import AsyncClient

from app.db.config import Base, test_async_session, test_engine

from ..main import app, get_session


async def override_get_session():
    try:
        db = test_async_session()
        yield db
    finally:
        await db.close()


async def init_models():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())

app.dependency_overrides[get_session] = override_get_session


@pytest.fixture
def user_payload(request):
    username = request.param.get("username", "test-user")
    return {
        "username": username,
        "fullname": f"{username} last",
        "email": f"{username}@example.com",
        "password": f"Pass{username}22#"
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("user_payload", [{"username": "user1"}], indirect=True)
async def test_signup_success(user_payload):
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post("/signup", json=user_payload)
        assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("user_payload", [{"username": "user2"}], indirect=True)
async def test_signup_failure_username_exists(user_payload):
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post("/signup", json=user_payload)
        assert response.status_code == 200
        response = await async_client.post("/signup", json=user_payload)
        assert response.status_code == 409
        assert response.json() == {"detail": "Username already in use."}


@pytest.mark.asyncio
@pytest.mark.parametrize("user_payload", [{"username": "user3"}], indirect=True)
async def test_signup_failure_email_exists(user_payload):
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post("/signup", json=user_payload)
        user_payload["username"] = "new_user"
        response = await async_client.post("/signup", json=user_payload)
        assert response.status_code == 409
        assert response.json() == {"detail": "Email already registered."}


@pytest.mark.asyncio
@pytest.mark.parametrize("user_payload", [{"username": "user3"}], indirect=True)
async def test_login_success(user_payload):
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post("/signup", json=user_payload)
        response = await async_client.post("/login",
                                           data={"username": user_payload["username"],
                                                 "password": user_payload["password"]})
        assert response.status_code == 200
        assert "access_token" in response.json()


@pytest.mark.asyncio
@pytest.mark.parametrize("user_payload", [{"username": "user5"}], indirect=True)
async def test_login_failure(user_payload):
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post("/signup", json=user_payload)
        response = await async_client.post(
            "/login", data={"username": user_payload["username"], "password": "wrong_password"})
        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect username or password."}
