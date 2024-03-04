from itertools import groupby
from operator import attrgetter

from models.track import Track
from schemas.track import TrackDetail, Disc
from services.base_service import BaseService


class TrackService(BaseService):
    """
    Класс бизнес-логики трека/песни
    """

    def __init__(self, db):
        super().__init__(db=db, model=Track)

    def is_tracks(self, album_id: int) -> bool:
        """
        Проверяет есть ли треки у альбома

        :param album_id: int
        :return: bool
        """

        if self.get_by_criteria(self._model.album_id == album_id).first():
            return True

        return False

    def create(self, track: Track) -> None:
        """
        Создает трек

        :param track: Track
        :return: None
        """

        self._db.add(track)
        self._db.commit()

    def split_by_disc(self, tracks: list[Track]) -> list[TrackDetail] | list[Disc]:
        """
        Разрезает треки альбома по дискам (если альбом состоит из нескольких дисков)

        :param tracks: list[Track]
        :return: list[TrackDetail] | list[Disc]
        """

        grouped_tracks = [(a, list(b)) for a, b in groupby(tracks, key=attrgetter('disc'))]

        if len(grouped_tracks) == 1:
            return [
                TrackDetail(
                    num=track.num, title=track.title, composers=track.composers,
                    performers=track.performers, duration=track.duration
                ) for track in grouped_tracks[0][1]
            ]
        else:
            result = []
            for item in grouped_tracks:
                track_detail = [
                    TrackDetail(
                        num=track.num, title=track.title, composers=track.composers,
                        performers=track.performers, duration=track.duration
                    ) for track in item[1]
                ]
                result.append(
                    Disc(label=item[0], items=track_detail)
                )
            return result
