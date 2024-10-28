from fastapi import FastAPI, Request,Form # improting fast api class 
from . import config 
from fastapi.responses import HTMLResponse
import pathlib
from . import shortcuts
from cassandra.cqlengine.management import sync_table 
from app.users.models import User
from .users.schemas import UserSignupSchema , UserLoginSchema
import json
from pydantic.v1.error_wrappers import ValidationError
from app.utilis import valid_schema_or_error
from .shortcuts import render
DB_SESSION = None # global variable e
app = FastAPI() # creating a object 

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
    return render(request,"auth/login.html",{
        "data":data,
        "errors":errors
    }
    )


@app.get("/signup",response_class=HTMLResponse) 
def login_get_view(request:Request):
    
    return render(request,"auth/signup.html",{
        # reguest must be pased to the template 
    }
    )
@app.post("/signup", response_class=HTMLResponse)
async def login_post_view(request: Request, email: str = Form(...), password: str = Form(...), password_confirm: str = Form(...)):
    raw_data = {
        "email":email,
        "password":password,
        "password_confirm":password_confirm
    }
    data , errors = valid_schema_or_error(raw_data,UserSignupSchema)
    
    return render(request,"auth/signup.html", {
        "data": data,
        "errors": errors
    })
