import uuid
from pydantic import BaseModel
from pydantic.v1 import (
    BaseModel,
)

from .models import Playlist
class playlistcreateshema(BaseModel):
    user_id : uuid.UUID # request.session user_id
    title : str

   