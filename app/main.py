from fastapi import FastAPI, Request,Form # improting fast api class 
from . import config 
from fastapi.responses import HTMLResponse
import pathlib
from fastapi.templating import Jinja2Templates
from cassandra.cqlengine.management import sync_table 
from app.users.models import User
from .users.schemas import UserSignupSchema
import json
from pydantic.v1.error_wrappers import ValidationError

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

DB_SESSION = None # global variable e
app = FastAPI() # creating a object 
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

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
        "request":request
    }
    return templates.TemplateResponse("home.html",context=context)

@app.get("/users")
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)



@app.get("/login",response_class=HTMLResponse) 
def login_get_view(request:Request):
    
    return templates.TemplateResponse("auth/login.html",{
        "request":request
    }
    )
@app.post("/login",response_class=HTMLResponse) 
def login_get_view(request:Request,email:str = Form(...),password : str = Form(...)):
    return templates.TemplateResponse("auth/login.html",{
        "request":request
    }
    )


@app.get("/signup",response_class=HTMLResponse) 
def login_get_view(request:Request):
    
    return templates.TemplateResponse("auth/signup.html",{
        "request":request # reguest must be pased to the template 
    }
    )
@app.post("/signup", response_class=HTMLResponse)
async def login_post_view(request: Request, email: str = Form(...), password: str = Form(...), password_confirm: str = Form(...)):
    errors = []
    data = {}
    
    try:
        cleaned_data = UserSignupSchema(email=email, password=password, password_confirm=password_confirm)
        data = cleaned_data.dict()  # Only if validation succeeds
        print("Cleaned Data:", data)
        
    except ValidationError as e:
        # Convert validation errors to JSON
        error_str = e.json()
        
        # Parse JSON errors
        try:
            errors = json.loads(error_str)
        except json.JSONDecodeError:
            errors = [{"loc": "non_field_error", "msg": "Unknown error"}]
        
        print("Errors:", errors)
    
    return templates.TemplateResponse("auth/signup.html", {
        "request": request,
        "data": data,
        "errors": errors
    })
