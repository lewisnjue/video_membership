from cassandra.cqlengine.models import Model
import uuid
from cassandra.cqlengine import columns
from app.config import get_settings
from . import validators , security
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
    
    def set_password(self,pw , commit = False):
        pw_hash = security.generate_hash(pw)
        self.password = pw_hash
        if commit:
            self.save()
        return True 
    def verify_password(self,pw):
        pw_hash = self.password
        verified , _ = security.verify_hash(pw_hash,pw)
        return verified    
    
    

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
        obj.set_password(password)
        #obj.password = password
        obj.save() 
        return obj 
    
    @staticmethod
    def check_exists(user_Id:uuid):
        q  = User.objects.filter(user_id = user_Id).allow_filtering()
        return q.count() != 0
    
    @staticmethod
    def by_user_id(user_id=None):
        if user_id is None:
            return None
        q  = User.objects.filter(user_Id = user_id).allow_filtering()
        if q.count() != 1:
            return None
        
        return q.first()
    



        



    