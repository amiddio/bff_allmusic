from typing import Optional
from beanie import Document


class User(Document):
    """
    Модель пользователя
    """

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
    """
    Модель пользователя для отображения
    """

    pass


class UserRegister(User):
    """
    Модель регистрации нового пользователя
    """

    password: str
    password_repeat: str


class UserInDB(User):
    """
    Модель пользователя для хранения в БД
    """

    hashed_password: str
