from fastapi import FastAPI # improting fast api class 



app = FastAPI() # creating a object 

@app.get("/") # this is routing not like in django 
def homepage():
    return {"hello":"world"}

