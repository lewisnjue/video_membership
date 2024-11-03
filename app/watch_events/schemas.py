from pydantic import BaseModel
import uuid
from typing import Optional

class WatchEventSchema(BaseModel):
    host_id : str 
    path : Optional[str]
    start_time : float
    end_time : float 
    complete : bool 



