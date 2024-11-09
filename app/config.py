import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"

class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent
    templates_dir: Path = Path(__file__).resolve().parent / "templates"
    keyspace: str 
    db_client_id: str 
    db_client_secret: str 
    secret_key: str
    jwt_algorithm: str 
    session_duration: int 
    algolia_app_id: str
    algolia_api_key: str
    algolia_index_name: str

    class Config:
        env_file = '.env'


@lru_cache
def get_settings():
    return Settings()
