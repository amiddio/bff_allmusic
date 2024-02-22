from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_URI_PREFIX: str

    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_USER: str
    MONGODB_PASS: str
    MONGODB_DB: str
    MONGODB_MAX_CONNECTIONS_COUNT: int

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env"
