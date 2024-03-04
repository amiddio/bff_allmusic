from typing import Any

from beanie import PydanticObjectId
from pydantic import BaseModel


class Crud:
    """
    Класс с различными CRUD операциями для моделей
    """

    @staticmethod
    async def create(model: Any) -> None:
        """
        Создание записи

        :param model: Any
        :return: None
        """

        await model.create()

    @staticmethod
    async def find(model: Any, criteria: Any = None) -> list[Any]:
        """
        Возвращает записи модели по условию

        :param model: Any
        :param criteria: Any
        :return: list[Any]
        """

        if criteria is None:
            criteria = {}
        return await model.find(criteria).to_list()

    @staticmethod
    async def find_one(model: Any, criteria: Any = None) -> Any:
        """
        Возвращает первую запись моделт по условию

        :param model: Any
        :param criteria: Any
        :return: Any
        """

        if criteria is None:
            criteria = {}
        return await model.find_one(criteria)

    @staticmethod
    async def get(model: Any, uid: PydanticObjectId) -> Any:
        """
        Возвращает запись модели по id

        :param model: Any
        :param uid: PydanticObjectId
        :return: Any
        """

        doc = await model.get(uid)
        return doc if doc else False

    @staticmethod
    async def delete(model: Any, uid: PydanticObjectId) -> bool:
        """
        Удаляет запись модели

        :param model: Any
        :param uid: PydanticObjectId
        :return: bool
        """

        doc = await model.get(uid)
        if not doc:
            return False
        await doc.delete()
        return True

    @staticmethod
    async def update(model: Any, uid: PydanticObjectId, data: BaseModel) -> Any:
        """
        Обновляет запись модели

        :param model: Any
        :param uid: PydanticObjectId
        :param data: BaseModel
        :return: Any
        """

        doc = await model.get(uid)
        if not doc:
            return False

        query = {
            "$set": {field: value for field, value in data.dict().items() if value is not None}
        }
        await doc.update(query)

        return doc
