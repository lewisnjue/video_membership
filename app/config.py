from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
import os 
os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"
class Settings(BaseSettings):
    base_dir : Path = Path(__file__).resolve().parent
    template_dir : Path = Path(__file__).resolve().parent /"templates"
    keyspace : str
    ASTRADB_CLIENT_ID : str
    ASTRADB_CLIENT_SECRET : str  
    secret_key : str    
    algorithm_jwt : str 
    session_duration : int 
    
    class Config:
        env_file = '.env'
        extra = "allow"  
@lru_cache
def get_settings():
    return Settings()
