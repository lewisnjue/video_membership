from pydantic.v1 import (
    BaseModel,
    validator,
    root_validator
)
from .extractors import extract_video_id
from app.users.exceptions import InvalidEmailException,UserIdException
from .exceptions import(
    InvalidYouTubeVideoUrlException,
    VideoAddedException
)
from .models import Video
class videocreateshema(BaseModel):
    url: str # user generated
    user_id : str # request.session user_id
    title : str

    @validator('url')
    def validate_youtube_url(cls,v,values,**kwargs):
        url = v
        video_id =  extract_video_id(url)
        if video_id is None:
            raise ValueError(f"{url} is not a valid youtube url")
        return url
    
    @root_validator
    def validate_data(cls,values):
        url = values.get('url')
        title = values.get('title')
        user_id = values.get('user_id')
        video_obj = None
        extra_data = {}
        if title is not None:
            extra_data['title'] = title

        

        try:
            video_obj = Video.add_video(url,user_id,**extra_data)

        except UserIdException :
            raise Exception("there is a problm with your account please try again")
        except InvalidYouTubeVideoUrlException:
            raise ValueError(f"{url} is not a valid youtube URL")
        except VideoAddedException:
            raise ValueError("the video has been added")
        if video_obj is None:
            raise Exception("there is a problm with your account please try again")
        if not isinstance(video_obj,Video):
            raise Exception("there is a problm with your account please try again")
      
        return video_obj.as_data()
    
    

    
    
class videoEditShema(BaseModel):
    url: str # user generated
    title : str

    @validator('url')
    def validate_youtube_url(cls,v,values,**kwargs):
        url = v
        video_id =  extract_video_id(url)
        if video_id is None:
            raise ValueError(f"{url} is not a valid youtube url")
        return url
    