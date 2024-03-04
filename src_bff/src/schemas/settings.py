from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    API_URI_PREFIX: str

    WEB_APP_ALLMUSIC_DOMAIN: str
    WEB_APP_USERS_DOMAIN: str
