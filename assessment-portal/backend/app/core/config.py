from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):

    # MongoDB
    MONGODB_URL: str
    DATABASE_NAME: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )


settings = Settings()