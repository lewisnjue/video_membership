from cassandra.cqlengine.models import Model
from app.users.models import User
from cassandra.cqlengine import columns
from .extractors import  extract_video_id
from app.config import get_settings
import uuid
from app.users.exceptions import UserIdException
from .exceptions import (InvalidYouTubeVideoUrlException,
                         VideoAddedException
                         
)
from cassandra.cqlengine.query import(
    DoesNotExist,
    MultipleObjectsReturned
)
from app.shortcuts import templates
settings = get_settings()

class Video(Model):
    __keyspace__ = settings.keyspace
    host_id = columns.Text(primary_key = True)
    host_service = columns.Text(default = 'youtube')
    db_id = columns.UUID(primary_key=True,default=uuid.uuid1)
    title = columns.Text()
    url = columns.Text()
    user_id = columns.UUID()

    def __str__(self):
        return f"title:{self.title},url{self.url}"
    
    def __repr__(self):
        return self.__str__()
    
    def render(self):
        basename = self.host_service
        template_name = f"videos/renderes/{basename}.html"
        context = {"host_id":self.host_id}
        t = templates.get_template(template_name)
        return t.render(context)
    

    def as_data(self):
        return {f"{self.host_service}_id":self.host_id,"path":self.path,"title":self.title}
    @property
    def  path(self):
        return f"/videos/{self.host_id}"
    
    @staticmethod
    def get_or_create(url, user_id=None, **kwargs):
        host_id = extract_video_id(url)
        obj = None
        created = False
        try:
            obj = Video.objects.get(host_id=host_id)
        except MultipleObjectsReturned:
            q = Video.objects.allow_filtering().filter(host_id=host_id)
            obj = q.first()
        except DoesNotExist:
            obj = Video.add_video(url, user_id=user_id, **kwargs)
            created = True
        except:
            raise Exception("Invalid Request")
        return obj, created
    
    def update_video_url(self,url,save=True):
        host_id = extract_video_id(url)
        if not host_id:
            return None
        self.url = url 
        self.host_id = host_id
        if save:
            self.save()
        return url 
    
    

    @staticmethod
    def add_video(url,user_id :  uuid =None,**kwargs):
        try :
            user_id = uuid.UUID(str(user_id))
        except Exception :
            error = " user id is not valid"
            return  UserIdException(error)
        host_id = extract_video_id(url=url)
        if host_id is None:
            raise InvalidYouTubeVideoUrlException(" invalid youtube video url")
        user_exits  = User.check_exists(user_id)
        if user_exits is None:
            raise UserIdException("invalid user id")
        q = Video.objects.allow_filtering().filter(host_id=host_id, user_id=user_id)

        if q.count() != 0:
            raise VideoAddedException("Video alredy added")
        return Video.create(host_id=host_id,user_id=user_id,url=url,**kwargs)


    


