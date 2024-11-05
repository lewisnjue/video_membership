from fastapi import APIRouter,Request,Form,Depends
from fastapi.responses import HTMLResponse
from  app.shortcuts import render,redirect,get_object_or_404,is_htmx
from app import utilis
from app.users.decorators import login_required
from .models import Playlist
from app.watch_events.models import WatchEvent
from .schemas import playlistcreateshema
from typing import Optional
import uuid
from .schemas import PlaylistVideoaddSchema
from starlette.exceptions import HTTPException
from typing import Optional
router = APIRouter(
    prefix='/playlists'
)

@router.get("/",response_class=HTMLResponse)
@login_required
def playlist_list_view(request:Request):
    q = list(Playlist.objects.all().limit(100))
    context = {
        "object_list":q
    }
    return  render(request,"playlists/list.html", context)

@router.get("/detail",response_class=HTMLResponse)
@login_required
def video_detail_view(request:Request):
    return render(request,"playlists/detail.html")


@router.get('/create',response_class=HTMLResponse)
@login_required
def playlist_create_view(request:Request):
    return render(request,"playlists/create.html",{})

@router.post('/create',response_class=HTMLResponse)
@login_required
def playlist_create_post_view(request:Request,title : str = Form(...)):
    raw_data = {
        "title":title,
        "user_id":request.user.username
    }
    data , errors = utilis.valid_schema_or_error(raw_data,playlistcreateshema)
    if len(errors) > 0:
        return render(request,"Playlists/create.html",{"errors":errors})
    obj = Playlist.objects.create(**data)
    
    redirect_path = obj.path or '/playlists/create'

    return redirect(redirect_path)

@router.get("/{db_id}",response_class=HTMLResponse)
def playlist_detail_view(request:Request,db_id: str):
    print("whatt this is funny please tell me am not dirmming")
    obj = get_object_or_404(Playlist,db_id=db_id)
    if request.user.is_authenticated:
        user_id = request.user.username
    context = {
        "object":obj,
        "videos":obj.get_videos()
    }
    return render(request,"playlists/detail.html",context)






@router.get('/{db_id}/add-video',response_class=HTMLResponse,)
@login_required
def playlist_vide_create_view(request:Request,is_htmx: bool = Depends(is_htmx),db_id : uuid.UUID = None):
    print(db_id)
    if not is_htmx:
        raise HTTPException(status_code=400)

    return render(request,"playlists/htmx/add-video.html",{"db_id":db_id})

@router.post('/{db_id}/add-video',response_class=HTMLResponse)
@login_required
def playlist_vide_create_post_view(request:Request,url : str =Form(...),title : str = Form(...),is_htmx: bool = Depends(is_htmx),db_id:uuid.UUID = None):
    raw_data = {
        "title":title,
        "url":url,
        "user_id":request.user.username,
        "playlist_id":db_id
    }
    data , errors = utilis.valid_schema_or_error(raw_data,PlaylistVideoaddSchema)
    redirect_path = data.get('path') or f'/playlists/{db_id}/'
  
    if not is_htmx:
        raise HTTPException(status_code=400)


    if len(errors) > 0:
        return render(request,"playlists/htmx/add-video.html",{"errors":errors,"db_id":db_id})
    context = {
        "path": redirect_path,
        "title": data.get("title")
        }
    return render(request,"videos/htmx/link.html",context)





@router.post("/{db_id}/{host_id}/delete/",response_class=HTMLResponse)
def playlist_remove_item_view(request:Request,db_id: str,host_id: str,index: Optional[int] = Form(default=None),is_htmx = Depends(is_htmx) ):
    if not is_htmx:
        raise HTTPException(status_code=400)
    try:
        obj = get_object_or_404(Playlist,db_id=db_id)
    except :
        return HTMLResponse("Error . Please reload the page")

    if not request.user.is_authenticated:
        return HTMLResponse("Please log in and continue")

    index = int(index)
  
    host_ids= obj.host_ids
    host_ids.pop(index)
    obj.add_host_ids(host_ids,replace_all=True) 
    obj.save()
    return HTMLResponse("Deleted")