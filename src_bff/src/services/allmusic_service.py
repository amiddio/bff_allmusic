from aiohttp import ClientSession
from starlette.datastructures import QueryParams

from services.base_service import BaseService


class AllmusicService(BaseService):
    """
    Методы бизнес-логики для взаимодействия с allmusic сервисом
    """

    async def get_all_artists(self, query_params: QueryParams) -> dict:
        """
        Возвращает список всех исполнителей разбитый на страницы

        :param query_params: QueryParams
        :return: dict
        """

        query_params = f'?{query_params}' if query_params else ''
        async with ClientSession() as session:
            return await self.get(
                session=session,
                url=self.APP_ALLMUSIC_DOMAIN + f'/view/artists{query_params}'
            )

    async def get_artist_by_id(self, artist_id: int) -> dict:
        """
        Возвращает исполнителя по его id

        :param artist_id: int
        :return: dict
        """

        async with ClientSession() as session:
            return await self.get(
                session=session,
                url=self.APP_ALLMUSIC_DOMAIN + f'/view/artist/{artist_id}'
            )

    async def is_artists_exist(self, artist_ids: dict) -> list[int | None]:
        """
        Возвращает список не существующих id исполнителей

        :param artist_ids: dict
        :return: list[int | None]
        """

        async with ClientSession() as session:
            resp_artist_ids = await self.post_json(
                session=session,
                url=self.APP_ALLMUSIC_DOMAIN + f'/view/is_artists',
                data=artist_ids
            )
            return list(set(artist_ids.get('artist_ids')).difference(resp_artist_ids))

    async def get_artist_albums(self, artist_id: int, release_type_id: int) -> dict:
        """
        Возвращает все альбомы исполнителя определенного типа (студийные, синглы и т.д.)

        :param artist_id: int
        :param release_type_id: int
        :return: dict
        """

        async with ClientSession() as session:
            return await self.get(
                session=session,
                url=self.APP_ALLMUSIC_DOMAIN + f'/view/discography/{artist_id}/{release_type_id}'
            )

    async def get_album_by_id(self, album_id: int) -> dict:
        """
        Возвращает информацию об альбоме по его id

        :param album_id: int
        :return: dict
        """

        async with ClientSession() as session:
            return await self.get(
                session=session,
                url=self.APP_ALLMUSIC_DOMAIN + f'/view/album/{album_id}'
            )

    async def get_artist_id(self, album_id: int) -> dict:
        """
        Возвращает id исполнителя по id альбома

        :param album_id: int
        :return: dict
        """

        async with ClientSession() as session:
            return await self.get(
                session=session,
                url=self.APP_ALLMUSIC_DOMAIN + f'/view/artist_id/{album_id}'
            )

    async def do_parsing(self, artists: dict) -> dict:
        """
        Запускает парсинг исполнителей

        :param artists: dict
        :return: dict
        """

        async with ClientSession() as session:
            return await self.post_json(
                session=session,
                url=self.APP_ALLMUSIC_DOMAIN + '/parser',
                data=artists,
                timeout=300
            )
