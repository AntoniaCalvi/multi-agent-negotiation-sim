from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field(default="development", alias="APP_ENV")
    simulation_max_rounds: int = Field(default=8, alias="SIMULATION_MAX_ROUNDS")
    default_discount_factor: float = Field(default=0.95, alias="DEFAULT_DISCOUNT_FACTOR")
    default_reservation_price: float = Field(default=0.45, alias="DEFAULT_RESERVATION_PRICE")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
