
from jose import jwt, ExpiredSignatureError
from .models import User
import datetime
from app import config

settings = config.get_settings()
def authenticate(email,password):
    try:
        user_ojb = User.objects.get(email = email)
        user_ojb.verify_password(password)
    except Exception:
        user_ojb = None
        return None
    
    return user_ojb
    

def login(user_obj,expires=5):
    data = {
    "user_id" :f"{user_obj.user_id}",
    "email":"do not do this ",
    "role":"admin",
    "exp":datetime.datetime.utcnow() + datetime.timedelta(seconds=expires)
    }
    return jwt.encode(data,settings.secret_key,algorithm=settings.algorithm_jwt)


def verify_user_id(token):
    data = None
    try:
        data = jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm_jwt])
    except ExpiredSignatureError as e:
        print(e)
    except Exception:
        pass
    if 'user_id' not in data:
        return None
    
    return data


