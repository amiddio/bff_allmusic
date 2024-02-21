from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_URI_PREFIX: str

    class Config:
        env_file = '.env'
