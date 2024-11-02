from fastapi import FastAPI, Request,Form ,HTTPException# improting fast api class 
from . import config 
from fastapi.responses import HTMLResponse
import pathlib
from . import shortcuts
from .shortcuts import redirect
from cassandra.cqlengine.management import sync_table 
from app.users.models import User
from .users.schemas import UserSignupSchema , UserLoginSchema
import json
from pydantic.v1.error_wrappers import ValidationError
from app.utilis import valid_schema_or_error
from .shortcuts import render
from .users.decorators import login_required
from app.users.exceptions import LoginRequiredException
from starlette.middleware.authentication import AuthenticationMiddleware
from .users.backends import JWTCookiesBackend
from .videos.models import Video
from .videos.routers import router as video_router



# from .handlers import http_exception_handler #noqa

app = FastAPI()

app.add_middleware(AuthenticationMiddleware,backend = JWTCookiesBackend())

app.include_router(video_router)

from .handlers import  all_exception


DB_SESSION = None


from . import db    

@app.on_event('startup')
def on_startup():
    db.get_session()
    global DB_SESSION
    DB_SESSION = db.get_session()
    print('startup')
    sync_table(User)
    sync_table(Video)



@app.get("/",response_class=HTMLResponse) # this is routing not like in django 
def homepage(request:Request):
    if request.user.is_authenticated:
        return render(request,"dashboard.html",{})

    return render(request,"home.html",{})

@app.get("/users")
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)



@app.get("/login",response_class=HTMLResponse) 
def login_get_view(request:Request):
    
    return render(request,"auth/login.html",{
    }
    )
@app.post("/login",response_class=HTMLResponse) 
def login_post_view(request:Request,email:str = Form(...),password : str = Form(...)):
    raw_data = {
        "email":email,
        "password":password,
    }
    data , errors = valid_schema_or_error(raw_data,UserLoginSchema)
    if len(errors) > 0 :
        raw_data = {
            "email":email,
            "password":password,
            "errors":errors

        }
        return render(request,"auth/login.html",raw_data)

    return  redirect('/',cookies=data)

@app.get("/signup",response_class=HTMLResponse) 
def signup_get_view(request:Request):
    
    return render(request,"auth/signup.html",{
        # reguest must be pased to the template 
    }
    )
@app.post("/signup", response_class=HTMLResponse)
async def signup_post_view(request: Request, email: str = Form(...), password: str = Form(...), password_confirm: str = Form(...)):
    raw_data = {
        "email":email,
        "password":password,
        "password_confirm":password_confirm
    }
    data , errors = valid_schema_or_error(raw_data,UserSignupSchema)
    print(data)

    
    return redirect('/login')





@app.get("/accounts",response_class=HTMLResponse)
@login_required
def account_view(request:Request):
    context ={}
    return render(request,"account.html",context=context)
