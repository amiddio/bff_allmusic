from typing import Any


class BaseService:

    def __init__(self, db, model):
        self._db = db
        self._model = model

    def get(self, iid: int) -> Any:
        """
        Возвращает объект модели по id

        :param iid: int
        :return: Any
        """
        return self._db.get(self._model, iid)

    def get_by_criteria(self, criteria) -> Any:
        """
        Возвращаем записи согласно условию

        :param criteria:
        :return: Any
        """

        return self._db.query(self._model).where(criteria)
