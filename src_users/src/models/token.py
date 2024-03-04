from pydantic import BaseModel


class Token(BaseModel):
    """
    Модель токена доступы
    """

    access_token: str
    token_type: str
