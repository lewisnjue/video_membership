import uuid
from pydantic import BaseModel

from pydantic.v1 import (
    BaseModel,
    validator,
    root_validator
)

from app.videos.extractors import extract_video_id
from app.users.exceptions import InvalidEmailException,UserIdException

from app.videos.models import Video

from .models import Playlist


class playlistcreateshema(BaseModel):
    user_id : uuid.UUID # request.session user_id
    title : str

    


class PlaylistVideoaddSchema(BaseModel):
    user_id : uuid.UUID # request.session user_id
    title : str
    url : str
    playlist_id : uuid.UUID

    @validator('url')
    def validate_youtube_url(cls,v,values,**kwargs):
        url = v
        video_id =  extract_video_id(url)
        if video_id is None:
            raise ValueError(f"{url} is not a valid youtube url")
        return url
    
    @validator('playlist_id')
    def validate_playlist_id(cls,v,values,**kwargs):
        q = Playlist.objects.filter(db_id = v)
        if q.count() == 0:
            raise ValueError(f"{v} is not a valid playlist")
        return  v


    @root_validator
    def validate_data(cls,values):
        url = values.get('url')
        title = values.get('title')
        user_id = values.get('user_id')
        playlist_id = values.get('playlist_id')

        extra_data = {}
        if title is not None:
            extra_data['title'] = title
        try:
            video_obj ,created= Video.get_or_create(url,user_id,**extra_data)
        except:
            raise Exception("there is a problm with your request please try again")
        if not isinstance(video_obj,Video):
            raise Exception("there is a problm with your account please try again")
        if playlist_id:
            playlist_obj = Playlist.objects.get(db_id = playlist_id)
            playlist_obj.add_host_ids(host_ids=[video_obj.host_id])
            playlist_obj.save()
      
        return video_obj.as_data()
    
    

    
    

   