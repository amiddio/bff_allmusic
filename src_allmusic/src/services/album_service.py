from fastapi import HTTPException
from sqlalchemy import and_
from starlette import status

from models import Album, Artist
from models.release_type import ReleaseType
from schemas.album import Albums, AlbumShort, AlbumDetail, AlbumDisplay
from schemas.artist import ArtistShort
from schemas.release_type import ReleaseTypeDetail
from services.artist_service import ArtistService
from services.base_service import BaseService
from services.release_type_service import ReleaseTypeService
from services.track_service import TrackService


class AlbumService(BaseService):
    """
    Класс бизнес-логики альбома
    """

    def __init__(self, db):
        super().__init__(db=db, model=Album)

    async def get_albums(self, artist_id: int, release_type_id: int) -> Albums:
        """
        Возвращает список альбомов исполнителя, отфильтрованных по релизам

        :param artist_id: int
        :param release_type_id: int
        :return: Albums
        """

        artist = ArtistService(db=self._db).get(iid=artist_id)
        if not artist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Artist with supplied ID does not exist"
            )

        release_type = ReleaseTypeService(db=self._db).get(iid=release_type_id)
        if not release_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Release type with supplied ID does not exist"
            )

        albums = self._db.query(self._model) \
            .where(and_(self._model.artist_id == artist_id, self._model.release_type_id == release_type_id)) \
            .order_by(self._model.id) \
            .all()

        return Albums(
            artist=ArtistShort(artist_id=artist.id, name=artist.name),
            release_type=ReleaseTypeDetail(
                release_type_id=release_type.id, type=release_type.type, name=release_type.name
            ),
            items=[AlbumShort(album_id=item.id, title=item.title, year=item.year) for item in albums]
        )

    async def get_album(self, album_id: int) -> AlbumDisplay:
        """
        Возвращает альбом и список песен

        :param album_id: int
        :return: AlbumDisplay
        """

        album = self._db.query(self._model) \
            .join(Artist, self._model.artist_id == Artist.id) \
            .join(ReleaseType, self._model.release_type_id == ReleaseType.id) \
            .where(self._model.id == album_id) \
            .first()
        if not album:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Album with supplied ID does not exist"
            )

        album_display = AlbumDetail(
            album_id=album.id, title=album.title, url=album.url, year=album.year, label=album.label,
            cover_url=album.cover_url, music_rating=album.music_rating, avg_rating=album.avg_rating,
            duration=album.duration, genre=album.genre, styles=album.styles
        )

        return AlbumDisplay(
            album=album_display,
            artist=ArtistShort(artist_id=album.artist.id, name=album.artist.name),
            tracks=TrackService(db=self._db).split_by_disc(tracks=album.tracks)
        )

    async def get_artist_id(self, album_id: int) -> int:
        """
        Возвращает artist id от переданого album id

        :param album_id: int
        :return: int
        """

        album = self._db.query(self._model.artist_id).where(self._model.id == album_id).first()
        if not album:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Album with supplied ID does not exist"
            )

        return album[0]

    def create_or_update(self, album: Album) -> int:
        """
        Создается или обновляется альбом в БД

        :param album: Album
        :return: int
        """

        row = self.get_by_criteria(and_(self._model.title == album.title, self._model.artist_id == album.artist_id))

        if row.first() is None:
            self._db.add(album)
        else:
            row.update({
                self._model.id: row.first().id,
                self._model.title: album.title,
                self._model.url: album.url,
                self._model.year: album.year,
                self._model.label: album.label,
                self._model.cover_url: album.cover_url,
                self._model.music_rating: album.music_rating,
                self._model.avg_rating: album.avg_rating
            })
        self._db.commit()

        return row.first().id

    def update(self, album_id: int, data: dict) -> None:
        """
        Обновляет поля альбома по id

        :param album_id: int
        :param data: dict
        :return: None
        """

        row = self.get_by_criteria(self._model.id == album_id)

        if row.first():
            row.update(data)
            self._db.commit()
