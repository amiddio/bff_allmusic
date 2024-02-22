from typing import Any

from beanie import PydanticObjectId
from pydantic import BaseModel


class Crud:

    @staticmethod
    async def create(model: Any) -> None:
        await model.create()

    @staticmethod
    async def find(model: Any, criteria: dict = None) -> list[Any]:
        if criteria is None:
            criteria = {}
        return await model.find(criteria).to_list()

    @staticmethod
    async def find_one(model: Any, criteria: dict = None) -> Any:
        if criteria is None:
            criteria = {}
        return await model.find_one(criteria)

    @staticmethod
    async def get(model: Any, uid: PydanticObjectId) -> Any:
        doc = await model.get(uid)
        return doc if doc else False

    @staticmethod
    async def delete(model: Any, uid: PydanticObjectId) -> bool:
        doc = await model.get(uid)
        if not doc:
            return False
        await doc.delete()
        return True

    @staticmethod
    async def update(model: Any, uid: PydanticObjectId, data: BaseModel) -> Any:
        doc = await model.get(uid)
        if not doc:
            return False

        query = {
            "$set": {field: value for field, value in data.dict().items() if value is not None}
        }
        await doc.update(query)

        return doc
