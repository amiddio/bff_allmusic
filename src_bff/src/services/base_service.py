from aiohttp import ClientSession
from fastapi import HTTPException
from starlette import status
from starlette.datastructures import Headers

from schemas.settings import Settings


class BaseService:

    APP_ALLMUSIC_DOMAIN = f"{Settings().WEB_APP_ALLMUSIC_DOMAIN}/api/v1"
    APP_USERS_DOMAIN = f"{Settings().WEB_APP_USERS_DOMAIN}/api/v1"

    @staticmethod
    async def get(session: ClientSession, url: str, headers: Headers = None) -> dict:
        async with session.get(url, headers=headers) as response:
            if response.status == status.HTTP_200_OK:
                return await response.json()

            error = await response.json()
            raise HTTPException(
                status_code=response.status,
                detail=error.get('detail', f"Url '{url}' not found")
            )

    @staticmethod
    async def post_json(session: ClientSession, url: str, data: dict) -> dict:
        async with session.post(url, json=data) as response:
            return await response.json()

    @staticmethod
    async def post_data(session: ClientSession, url: str, data: dict) -> dict:
        async with session.post(url, data=data) as response:
            return await response.json()
