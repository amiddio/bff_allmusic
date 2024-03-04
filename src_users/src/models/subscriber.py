from datetime import datetime
from beanie import Document, Link
from pydantic import BaseModel

from models.user import UserOut


class Subscriber(Document):
    """
    Модель подписки пользователя на исполнителя
    """

    user: Link[UserOut]
    artist_id: int
    active_till: datetime

    class Settings:
        name = 'subscriber_collection'

    model_config = {
        'json_schema_extra': {
            'example': {
                'user_id': 5,
                'artist_id': 114,
                'active_till': datetime,
            }
        }
    }


class SubscribeFormData(BaseModel):
    """
    Модель входящих данных для подписки на исполнителей
    """

    artist_ids: list[int]
    days: int


class Subscriptions(BaseModel):
    """
    Модель списка подписок
    """

    subscriptions: list[Subscriber]
