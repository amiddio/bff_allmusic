from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from models.settings import Settings


class AuthJWT:
    """
    Класс для работы с Json Web Token
    """

    settings = Settings()
    password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def get_hashed_password(self, password: str) -> str:
        """
        Метод возвращает хеширует пароль

        :param password: str
        :return: str
        """

        return self.password_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Проверка пароля на валидность

        :param password: str
        :param hashed_password: str
        :return: bool
        """

        return self.password_context.verify(password, hashed_password)

    def create_access_token(self, subject: str, expires_delta: int = None) -> str:
        """
        Метод возвращает токен доступа

        :param subject: str
        :param expires_delta: int
        :return: str
        """

        return self.__class__.__create_token(
            subject, self.settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES, self.settings.JWT_SECRET_KEY, expires_delta
        )

    def decode_token(self, token: str) -> dict:
        """
        Метод декодирует токен

        :param token: str
        :return: dict
        """

        return jwt.decode(token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ALGORITHM])

    @classmethod
    def __create_token(cls, subject: str, token_expires: int, secret_key: str, expires_delta: int = None) -> str:
        """
        Метод создает токен

        :param subject: str
        :param token_expires: int
        :param secret_key: str
        :param expires_delta: int
        :return: str
        """

        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=token_expires)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, secret_key, cls.settings.JWT_ALGORITHM)
        return encoded_jwt
