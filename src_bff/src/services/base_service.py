from aiohttp import ClientSession
from fastapi import HTTPException
from starlette import status

from schemas.settings import Settings


class BaseService:

    APP_ALLMUSIC_DOMAIN = f"{Settings().WEB_APP_ALLMUSIC_DOMAIN}{Settings().API_URI_PREFIX}"

    @staticmethod
    async def get(session: ClientSession, url: str) -> dict:
        async with session.get(url) as response:
            if response.status == status.HTTP_200_OK:
                return await response.json()

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Url '{url}' not found"
            )

    @staticmethod
    async def post(session: ClientSession, url: str, data: dict) -> dict:
        async with session.post(url, json=data) as response:
            return await response.json()
