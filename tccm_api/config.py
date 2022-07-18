import os
from functools import lru_cache
from pathlib import Path
from pprint import pprint

from pydantic import BaseSettings, ValidationError


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
    """get_settings"""
    env_file_path = os.path.join(ROOT_DIR, '.env')
    try:
        settings = Settings(_env_file=env_file_path)
        return settings
    except ValidationError as err:
        print('Env files not found?:')
        print('env_file_path:', env_file_path)
        exists = '.env' in os.listdir()
        pprint(os.listdir(ROOT_DIR))
        print('env file exists?:', exists)
        if exists:
            'env file contents: '
            with open(env_file_path, 'r') as file:
                print(file.read())
        raise err
