import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture(scope="session")
async def login(client: AsyncClient):
    input_data = {
        "username": "tester.testerovich@home.com",
        "password": "qwerty"
    }
    return await client.post("/users/login", data=input_data)
