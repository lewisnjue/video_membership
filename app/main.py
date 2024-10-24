from fastapi import FastAPI # improting fast api class 
from . import config 
from cassandra.cqlengine.management import sync_table 
from .users.models import User #
from app.users.models import User
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


@app.get("/") # this is routing not like in django 
def homepage():
    return {"hello":"world"}

