from fastapi import FastAPI, Request,Form ,HTTPException# improting fast api class 
from . import config 
from fastapi.responses import HTMLResponse
import pathlib
from starlette.exceptions import HTTPException as Starlette
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
# from .handlers import http_exception_handler #noqa


app = FastAPI()

# -> the bolow code should not be there think about it 

@app.exception_handler(LoginRequiredException)
async def login_required_exception_handler(request,exc):
    return redirect(f'/login?next={request.url}',remove_session=True)

@app.exception_handler(Starlette)
async def login_required_exception_handler(request,exc):
    status_code = exc.status_code 
    template_name = 'errors/main.html'
    if status_code == 404:
        template_name = 'errors/404.html'

    context = {"status_code":status_code}
    return render(request=request,template_name=template_name,context=context)
# upto here 

DB_SESSION = None


from . import db    

@app.on_event('startup')
def on_startup():
    db.get_session()
    global DB_SESSION
    DB_SESSION = db.get_session()
    print('startup')
    sync_table(User)


@app.get("/",response_class=HTMLResponse) # this is routing not like in django 
def homepage(request:Request):
    context ={
       
    }
    return render(request,"home.html",context=context)

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