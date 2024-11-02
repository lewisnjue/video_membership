from cassandra.cqlengine.models import Model

from cassandra.cqlengine import columns

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
    

