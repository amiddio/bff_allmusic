from fastapi import HTTPException
from starlette import status

from models.artist import Artist
from models.release_type import ReleaseType
from schemas.artist import ArtistShort, ArtistDetail
from schemas.pagination import PagedResponseSchema, PageParams
from schemas.release_type import ReleaseTypeDetail
from services.base_service import BaseService
from services.release_type_service import ReleaseTypeService


class ArtistService(BaseService):

    def __init__(self, db):
        super().__init__(db=db, model=Artist)

    async def get_all(self, page_params: PageParams) -> PagedResponseSchema:
        """
        Возвращает список исполнителей с разбиением на страницы

        :param page_params: PageParams
        :return: PagedResponseSchema
        """

        query = self._db.query(self._model)

        paginated_query = query.order_by(self._model.name) \
            .offset((page_params.page - 1) * page_params.size) \
            .limit(page_params.size).all()

        return PagedResponseSchema(
            total=query.count(),
            page=page_params.page,
            size=page_params.size,
            items=[ArtistShort(artist_id=item.id, name=item.name) for item in paginated_query],
        )

    async def get_artist_by_id(self, artist_id: int) -> ArtistDetail:
        """
        Возвращает исполнителя по id, и список типов релизов (студийные альбомы, синглы и т.д.)

        :param artist_id: int
        :return: ArtistDetail
        """

        artist = self.get(iid=artist_id)
        if not artist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Artist with supplied ID does not exist"
            )

        release_types = ReleaseTypeService(db=self._db).get_artist_release_types(artist_id=artist_id)

        return ArtistDetail(
            artist_id=artist.id, name=artist.name, url=artist.url, genres=artist.genres, decades=artist.decades,
            release_types=[
                ReleaseTypeDetail(release_type_id=item.id, type=item.type, name=item.name) for item in release_types
            ],
        )

    async def is_artists(self, artist_ids: list[int]) -> list[int]:
        """
        Возвращает список artist_id которые есть в БД

        :param artist_ids: list[int]
        :return: list[int]
        """

        ids = self._db.query(self._model.id).where(self._model.id.in_(artist_ids)).all()
        return list(map(lambda x: int(x[0]), ids))

    def create_or_update(self, artist: Artist) -> int:
        """
        Создается или обновляется исполнитель в БД

        :param artist: Artist
        :return: int
        """

        row = self.get_by_criteria(self._model.name == artist.name)

        if row.first() is None:
            self._db.add(artist)
        else:
            row.update(
                {self._model.url: artist.url, self._model.genres: artist.genres, self._model.decades: artist.decades}
            )
        self._db.commit()

        return row.first().id
