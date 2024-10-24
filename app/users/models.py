from cassandra.cqlengine.models import Model
import uuid
from cassandra.cqlengine import columns
from app.config import get_settings

settings = get_settings()
keyspace = settings.keyspace


class User(Model):
    __keyspace__ = keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()


    def __repr__(self):
        return f"user ('{self.email}', '{self.user_id}', '{self.password}')"
    
    def __str__(self):
        return self.__repr__()
    