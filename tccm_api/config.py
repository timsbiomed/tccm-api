from functools import lru_cache
from pathlib import Path
from pydantic import BaseSettings
import sys

ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    app_name: str = 'TCCM API'
    neo4j_username: str
    neo4j_password: str
    neo4j_bolt_port: int
    neo4j_host: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
