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


