from functools import lru_cache
from typing import Literal

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

  app_name: str = Field("DeepScan", alias="APP_NAME")
  app_env: Literal["development", "staging", "production"] = Field(
    "development", alias="APP_ENV"
  )
  app_host: str = Field("0.0.0.0", alias="APP_HOST")
  app_port: int = Field(8000, alias="APP_PORT")

  database_url: AnyUrl = Field(
    "postgresql+asyncpg://deepscan:deepscan@localhost:5432/deepscan", alias="DATABASE_URL"
  )

  log_level: str = Field("info", alias="LOG_LEVEL")


@lru_cache
def get_settings() -> Settings:
  return Settings()  # type: ignore[call-arg]


settings = get_settings()

