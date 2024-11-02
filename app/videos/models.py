from cassandra.cqlengine.models import Model
from app.users.models import User
from cassandra.cqlengine import columns
from .extractors import  extract_video_id
from app.config import get_settings
import uuid
settings = get_settings()

class Video(Model):
    __keyspace__ = settings.keyspace
    host_id = columns.Text(primary_key = True)
    host_service = columns.Text(default = 'youtube')
    db_id = columns.UUID(primary_key=True,default=uuid.uuid1)
    url = columns.Text()
    user_id = columns.UUID()

    @staticmethod
    def add_video(url,user_id :  uuid =None):
        try :
            user_id = uuid.UUID(str(user_id))
        except Exception : 
            raise Exception("user id is not valid")
        

        host_id = extract_video_id(url=url)
        if host_id is None:
            raise Exception(" invalid youtube video url")
        user_exits  = User.check_exists(user_id)
        if user_exits is None:
            raise Exception("invalid user id")
        q = Video.objects.allow_filtering().filter(host_id=host_id, user_id=user_id)

        if q.count() != 0:
            raise Exception("Video alredy added")
        return Video.create(host_id=host_id,user_id=user_id,url=url)


    

