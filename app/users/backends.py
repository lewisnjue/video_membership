from . import auth 
from starlette.authentication  import (
    AuthenticationBackend,
    SimpleUser,
    UnauthenticatedUser,
    AuthCredentials
)

class JWTCookiesBackend(AuthenticationBackend):
    async def authenticate(self,request):
        try :
            session_id = request.cookies.get('session_id')
            user_data = auth.verify_user_id(session_id)
            user_id  = user_data.get('user_id')
            roles = ['authenticated']
            return AuthCredentials(roles),SimpleUser(user_id) # this is what will be request.user
        
        except Exception:
            roles = ['annon']
            return AuthCredentials(roles) , UnauthenticatedUser()

