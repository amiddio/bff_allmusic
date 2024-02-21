from models import Album
from models.release_type import ReleaseType
from services.base_service import BaseService


class ReleaseTypeService(BaseService):

    def __init__(self, db):
        super().__init__(db=db, model=ReleaseType)

    def get_release_type(self, release_type: str, name: str) -> ReleaseType:
        """
        Возвращает тип релиза по условию. Если его не существует, то создается.

        :param release_type: str
        :param name: str
        :return: ReleaseType
        """

        row = self.get_by_criteria(self._model.type == release_type)

        if row.first() is None:
            self._db.add(ReleaseType(type=release_type, name=name))
            self._db.commit()
            return self.get_by_criteria(self._model.type == release_type).first()
        else:
            return row.first()

    def get_artist_release_types(self, artist_id: int) -> list[ReleaseType]:
        """
        Вовращает список типов релиза связанных с исполнителем и альбомами

        :param artist_id: int
        :return: list[ReleaseType]
        """

        return self._db.query(self._model) \
            .join(Album, self._model.id == Album.release_type_id) \
            .where(Album.artist_id == artist_id) \
            .order_by(self._model.id) \
            .distinct() \
            .all()
