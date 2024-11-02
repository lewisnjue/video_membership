from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from  app.shortcuts import render

from app.users.decorators import login_required
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
