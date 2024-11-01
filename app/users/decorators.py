from functools import wraps
from fastapi import Request
from .auth import verify_user_id

from .exceptions import LoginRequiredException

def login_required(func):
    @wraps(func)
    def wrapper(request: Request, *args,**kwargs):
        session = request.cookies.get('session_id')

        if not session : 
            raise LoginRequiredException(status_code=401)
        
        user_session = verify_user_id(session)
        if user_session is None:
            raise LoginRequiredException(status_code=401)
        

        return func(request,*args,**kwargs)
    
    return wrapper
