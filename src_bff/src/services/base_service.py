from aiohttp import ClientSession
from fastapi import HTTPException
from starlette import status
from starlette.datastructures import Headers

from schemas.settings import Settings


class BaseService:
    """
    Базовый класс содержащий общий функционал для различных сервисов
    """

    APP_ALLMUSIC_DOMAIN = f"{Settings().WEB_APP_ALLMUSIC_DOMAIN}"
    APP_USERS_DOMAIN = f"{Settings().WEB_APP_USERS_DOMAIN}"
    TIMEOUT = 3

    @staticmethod
    async def get(session: ClientSession, url: str, headers: Headers = None) -> dict:
        """
        Выполняется GET запрос

        :param session: ClientSession
        :param url: str
        :param headers: Headers
        :return: dict
        """

        async with session.get(url, timeout=BaseService.TIMEOUT, headers=headers) as response:
            if response.status == status.HTTP_200_OK:
                return await response.json()

            error = await response.json()
            raise HTTPException(
                status_code=response.status,
                detail=error.get('detail', f"Url '{url}' not found")
            )

    @staticmethod
    async def post_json(
        session: ClientSession, url: str, data: dict, headers: Headers = None, timeout: int = TIMEOUT
    ) -> dict:
        """
        Выполняется POST запрос

        :param session: ClientSession
        :param url: str
        :param data: dict
        :param headers: Headers
        :param timeout: int
        :return: dict
        """

        async with session.post(url, json=data, timeout=timeout, headers=headers) as response:
            return await response.json()

    @staticmethod
    async def post_data(
        session: ClientSession, url: str, data: dict, headers: Headers = None, timeout: int = TIMEOUT
    ) -> dict:
        """
        Выполняется POST запрос

        :param session: ClientSession
        :param url: str
        :param data: dict
        :param headers: Headers
        :param timeout: int
        :return: dict
        """

        async with session.post(url, data=data, timeout=timeout, headers=headers) as response:
            return await response.json()
