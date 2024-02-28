from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    API_URI_PREFIX: str

    DB_TYPE: str
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    PGADMIN_EMAIL: str
    PGADMIN_PASSW: str
