from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_URI_PREFIX: str

    DB_TYPE: str
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    PGADMIN_EMAIL: str
    PGADMIN_PASSW: str

    class Config:
        env_file = '.env'
