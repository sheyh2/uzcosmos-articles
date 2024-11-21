import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_URL: str
    APP_PORT: str
    UPLOAD_DIR: str

    DB_CONNECTION: str
    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str

    class Config:
        env_file = '.env'


settings = Settings()
DATABASE_URL = f'{settings.DB_CONNECTION}://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}'

if not os.path.exists(settings.UPLOAD_DIR):
    os.mkdir(settings.UPLOAD_DIR)


def asset(path: str = None) -> str:
    base_url = settings.APP_URL
    if path is None:
        return base_url
    return f'{base_url}/{path}'
