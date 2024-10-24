from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache
import pathlib 
import os 
BASE_DIR = pathlib.Path(__file__).resolve().parent
os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"
class Settings(BaseSettings):
    keyspace : str
    ASTRADB_CLIENT_ID : str
    ASTRADB_CLIENT_SECRET : str  
    
    class Config:
        env_file = '.env'
        extra = "allow"  
@lru_cache
def get_settings():
    return Settings()
