from datetime import datetime

from beanie import Document, Indexed, Link
from pydantic import BaseModel

from models.user import User, UserOut


class Subscriber(Document):
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
    artist_ids: list[int]
    days: int


class Subscriptions(BaseModel):
    subscriptions: list[Subscriber]
