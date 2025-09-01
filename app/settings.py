from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    mongodb_uri: str = (
        "mongodb://localhost:27017"
    )
    mongodb_db: str = "app"
    mongodb_collection: str = "records"

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "info"


@lru_cache()
def getSettings() -> AppSettings:
    return AppSettings()

