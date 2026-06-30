from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "WealthPilot Autonomous Portfolio Rebalancer"
    VERSION: str = "1.0.0"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Gemini
    GOOGLE_API_KEY: str = Field(default="")

    DATABASE_URL: str = "sqlite:///wealthpilot.db"

    VECTOR_DB_PATH: str = "./memory/vector_db"

    DRIFT_THRESHOLD: float = 0.05

    REBALANCE_INTERVAL_DAYS: int = 90

    MAX_TAX_PERCENT: float = 0.20

    MAX_SECTOR_WEIGHT: float = 0.30

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings():

    return Settings()


settings = get_settings()