from fastapi import APIRouter,Request,Form,Depends
from fastapi.responses import HTMLResponse
from  app.shortcuts import render,redirect,get_object_or_404,is_htmx
from app import utilis
from app.users.decorators import login_required
from .schemas import videocreateshema , videoEditShema
from .models import Video
from app.watch_events.models import WatchEvent
from typing import Optional
import uuid
from starlette.exceptions import HTTPException

router = APIRouter(
    prefix='/videos'
)

@router.get("/",response_class=HTMLResponse)
@login_required
def video_list_view(request:Request):
    q = list(Video.objects.all().limit(100))
    context = {
        "object_list":q
    }
    return  render(request,"videos/list.html", context)

@router.get("/detail",response_class=HTMLResponse)
@login_required
def video_detail_view(request:Request):
    return render(request,"videos/detail.html")




@router.get('/create',response_class=HTMLResponse,)
@login_required
def vide_create_view(request:Request,is_htmx: bool = Depends(is_htmx),playlist_id: Optional[uuid.UUID] =None ):
    print(playlist_id)
    if is_htmx:
        return render(request,"videos/htmx/create.html",{})

    return render(request,"videos/create.html",{})

@router.post('/create',response_class=HTMLResponse)
@login_required
def vide_create_post_view(request:Request,url : str =Form(...),title : str = Form(...),is_htmx: bool = Depends(is_htmx)):
    raw_data = {
        "title":title,
        "url":url,
        "user_id":request.user.username
    }
    data , errors = utilis.valid_schema_or_error(raw_data,videocreateshema)
    redirect_path = data.get('path') or '/videos/create'
  
    if is_htmx:
        context = {
            "path": redirect_path,
            "title": data.get("title")
        }
         
        if len(errors) > 0:
            return render(request,"videos/htmx/create.html",{"errors":errors})
    
        return render(request,"videos/htmx/link.html",context)
  
    if len(errors) > 0:
        return render(request,"videos/create.html",{"errors":errors})
    
    

    return redirect(redirect_path)

@router.get("/{host_id}",response_class=HTMLResponse)
def video_detail_view(request:Request,host_id: str):
    obj = get_object_or_404(Video,host_id=host_id)
    start_time = 0 
    if request.user.is_authenticated:
        user_id = request.user.username
        start_time = WatchEvent.get_resume_time(host_id,user_id)
    context = {
        "host_id":host_id,
        "object":obj,
        "start_time":start_time,
    }
    return render(request,"videos/detail.html",context)



@router.get("/{host_id}/hx-edit",response_class=HTMLResponse)
@login_required
def video_hx_edit_view(request:Request,
                       host_id: str,
                       is_htmx = Depends(is_htmx),
                       obj = None,
                      
                       ):
    not_found = False
    if not is_htmx:
        raise HTTPException(status_code=400)
    try:
        obj = get_object_or_404(Video,host_id=host_id)
    except:
        not_found = True
    if  not_found:
        return HTMLResponse("Not Found , Please try agin ")

    context = {
        "host_id":host_id,
        "object":obj
    }
    return render(request,"videos/htmx/edit.html",context)



@router.post("/{host_id}/hx-edit",response_class=HTMLResponse)
@login_required
def vide_hx_edit_post_view(
    request:Request,
    host_id: str,
    delete : Optional[bool] = Form(default=False),
    url : str =Form(...),
    title : str = Form(...),
    is_htmx: bool = Depends(is_htmx)):
    raw_data = {
        "title":title,
        "url":url,
    }
    not_found = False
    if not is_htmx:
        raise HTTPException(status_code=400)
    try:
        obj = get_object_or_404(Video,host_id=host_id)
    except:
        not_found = True
    if  not_found:
        return HTMLResponse("Not Found , Please try agin ")
    
    if delete:
        obj.delete()
        return HTMLResponse("Item deleted ")

    data , errors = utilis.valid_schema_or_error(raw_data,videoEditShema)
    context = {
        "object":obj
    }
    if len(errors) > 0:
        return render(request,"videos/htmx/edit.html",context={"errors":errors,"object":obj})
    
    obj.title = data.get('title') or obj.title
    obj.update_video_url(url,save=True)
    return render(request,"videos/htmx/list-inline.html",context=context)





@router.post("/{host_id}/edit",response_class=HTMLResponse)
@login_required
def vide_edit_post_view(
    request:Request,
    host_id: str,
    url : str =Form(...),
    title : str = Form(...),
    is_htmx: bool = Depends(is_htmx)):
    raw_data = {
        "title":title,
        "url":url,
    }
    obj = get_object_or_404(Video,host_id=host_id)
    data , errors = utilis.valid_schema_or_error(raw_data,videoEditShema)
    context = {
        "object":obj
    }
    if len(errors) > 0:
        return render(request,"videos/edit.html",context={"errors":errors,"object":obj})
    
    obj.title = data.get('title') or obj.title
    obj.update_video_url(url,save=True)
    return render(request,"videos/edit.html",context=context)



@router.get("/{host_id}/edit",response_class=HTMLResponse)
@login_required
def video_edit_view(request:Request,host_id: str):
    obj = get_object_or_404(Video,host_id=host_id)
    context = {
        "host_id":host_id,
        "object":obj
    }
    return render(request,"videos/edit.html",context)

