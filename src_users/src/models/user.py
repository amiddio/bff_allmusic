from typing import Optional

from beanie import Document


class User(Document):
    email: str
    name: Optional[str] = None
    is_active: Optional[str] = None

    class Settings:
        name = 'user_collection'

    model_config = {
        'json_schema_extra': {
            'example': {
                'email': "some_email@home.local",
                'name': "John Dow",
                'is_active': "Bool value active a user or not",
            },
        }
    }


class UserOut(User):
    pass


class UserRegister(User):
    password: str
    password_repeat: str


class UserInDB(User):
    hashed_password: str
