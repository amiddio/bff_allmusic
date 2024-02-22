from aiohttp import ClientSession
from starlette.datastructures import QueryParams

from services.base_service import BaseService


class AllmusicService(BaseService):

    async def get_all_artists(self, query_params: QueryParams) -> dict:
        query_params = f'?{query_params}' if query_params else ''
        async with ClientSession() as session:
            return await self.__class__.get(
                session=session,
                url=self.__class__.APP_ALLMUSIC_DOMAIN + f'/view/artists{query_params}'
            )

    async def get_artist_by_id(self, artist_id: int) -> dict:
        async with ClientSession() as session:
            return await self.__class__.get(
                session=session,
                url=self.__class__.APP_ALLMUSIC_DOMAIN + f'/view/artist/{artist_id}'
            )

    async def get_artist_albums(self, artist_id: int, release_type_id: int) -> dict:
        async with ClientSession() as session:
            return await self.__class__.get(
                session=session,
                url=self.__class__.APP_ALLMUSIC_DOMAIN + f'/view/discography/{artist_id}/{release_type_id}'
            )

    async def get_album_by_id(self, album_id: int) -> dict:
        async with ClientSession() as session:
            return await self.__class__.get(
                session=session,
                url=self.__class__.APP_ALLMUSIC_DOMAIN + f'/view/album/{album_id}'
            )

    async def do_parsing(self, artists: dict):
        async with ClientSession() as session:
            return await self.__class__.post(
                session=session,
                url=self.__class__.APP_ALLMUSIC_DOMAIN + '/parser',
                data=artists
            )