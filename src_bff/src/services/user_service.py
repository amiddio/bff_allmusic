from aiohttp import ClientSession
from starlette.datastructures import Headers

from services.base_service import BaseService


class UserService(BaseService):

    async def register_user(self, user_data: dict) -> dict:
        async with ClientSession() as session:
            return await self.post_json(
                session=session,
                url=self.APP_USERS_DOMAIN + '/users/register',
                data=user_data
            )

    async def login_user(self, login_data: dict) -> dict:
        async with ClientSession() as session:
            return await self.post_data(
                session=session,
                url=self.APP_USERS_DOMAIN + '/users/login',
                data=login_data
            )

    async def get_user(self, headers: Headers) -> dict:
        async with ClientSession() as session:
            return await self.get(
                session=session,
                url=self.APP_USERS_DOMAIN + '/users/me',
                headers=headers
            )

    async def is_permission(self, artist_id: int, headers: Headers):
        async with ClientSession() as session:
            return await self.get(
                session=session,
                url=self.APP_USERS_DOMAIN + f'/users/is_permission/{artist_id}',
                headers=headers
            )

    async def subscribe_user(self, data: dict, headers: Headers) -> dict:
        header_authorization = {'Authorization': headers.get('Authorization')}
        async with ClientSession(headers=header_authorization) as session:
            return await self.post_json(
                session=session,
                url=self.APP_USERS_DOMAIN + '/subscribe',
                data=data
            )
