from cassandra.cqlengine.models import Model
import uuid
from cassandra.cqlengine import columns
from app.config import get_settings
from . import validators 
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
    

    @staticmethod
    def create_user(email,password=None):
        # check if their is an email in the database arelady 
        q = User.objects.filter(email=email) 
        if q.count() != 0:
            raise Exception("user already has account")
        valid , msg , email = validators._validate_email(email)
        if not valid:
            raise Exception(msg)
        obj = User(email= email)
        obj.password = password
        obj.save() 
        return obj 
    

    