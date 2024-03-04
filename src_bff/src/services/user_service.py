from aiohttp import ClientSession
from starlette.datastructures import Headers

from services.base_service import BaseService


class UserService(BaseService):
    """
    Методы бизнес-логики для взаимодействия с сервисом пользователей
    """

    async def register_user(self, user_data: dict) -> dict:
        """
        Метод регистрации нового пользователя

        :param user_data: dict
        :return: dict
        """

        async with ClientSession() as session:
            return await self.post_json(
                session=session,
                url=self.APP_USERS_DOMAIN + '/users/register',
                data=user_data
            )

    async def login_user(self, login_data: dict) -> dict:
        """
        Метод авторизации пользователя

        :param login_data: dict
        :return: dict
        """

        async with ClientSession() as session:
            return await self.post_data(
                session=session,
                url=self.APP_USERS_DOMAIN + '/users/login',
                data=login_data
            )

    async def get_user(self, headers: Headers) -> dict:
        """
        Возвращает данные о пользователе по токену

        :param headers: Headers
        :return: dict
        """

        async with ClientSession() as session:
            return await self.get(
                session=session,
                url=self.APP_USERS_DOMAIN + '/users/me',
                headers=headers
            )

    async def is_permission(self, artist_id: int, headers: Headers) -> dict:
        """
        Метод проверяет есть ли у пользователя права для просмотра исполнителя

        :param artist_id: int
        :param headers: Headers
        :return: dict
        """

        async with ClientSession() as session:
            return await self.get(
                session=session,
                url=self.APP_USERS_DOMAIN + f'/users/is_permission/{artist_id}',
                headers=headers
            )

    async def subscribe_user(self, data: dict, headers: Headers) -> dict:
        """
        Метод подписывает текущего пользователя (авторизованного по токену) на исполнителей.
        Ids исполнителей передаются списком

        :param data: dict
        :param headers: Headers
        :return: dict
        """

        header_authorization = {'Authorization': headers.get('Authorization')}
        async with ClientSession(headers=header_authorization) as session:
            return await self.post_json(
                session=session,
                url=self.APP_USERS_DOMAIN + '/subscribe',
                data=data
            )
