from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_URI_PREFIX: str

    WEB_APP_ALLMUSIC_DOMAIN: str

    class Config:
        env_file = '.env'
