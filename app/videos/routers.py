from fastapi import APIRouter,Request,Form
from fastapi.responses import HTMLResponse
from  app.shortcuts import render,redirect
from app import utilis
from app.users.decorators import login_required
from .schemas import videocreateshema
router = APIRouter(
    prefix='/videos'
)

@router.get("/",response_class=HTMLResponse)
@login_required
def video_list_view(request:Request):
    return  render(request,"videos/list.html", {})

@router.get("/detail",response_class=HTMLResponse)
@login_required
def video_detail_view(request:Request):
    return render(request,"videos/detail.html")


@router.get('/create',response_class=HTMLResponse)
@login_required
def vide_create_view(request:Request):
    return render(request,"videos/create.html",{})

@router.post('/create',response_class=HTMLResponse)
@login_required
def vide_create_post_view(request:Request,url : str =Form(...)):
    raw_data = {
        "url":url,
        "user_id":request.user.username
    }
    data , errors = utilis.valid_schema_or_error(raw_data,videocreateshema)
    if len(errors) > 0:
        return render(request,"videos/create.html",{"errors":errors})
    
    redirect_path = data.get('path') or '/videos/create'

    return redirect(redirect_path)

