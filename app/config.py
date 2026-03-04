# config.py

from pydantic import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "CyberScope"
    VERSION: str = "1.0"

    DATABASE_URL: str = "sqlite:///./cyberscope.db"

    MAX_CIDR_SIZE: int = 256
    PING_TIMEOUT: int = 1

    class Config:
        env_file = ".env"


settings = Settings()