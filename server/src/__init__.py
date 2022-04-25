from pydantic import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    MYSQL_DB_URL: str
    SECRET_KEY: str
    ALGORITHM: str


@lru_cache()
def get_settings():
    return Settings()
