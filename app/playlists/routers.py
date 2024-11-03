from fastapi import APIRouter,Request,Form
from fastapi.responses import HTMLResponse
from  app.shortcuts import render,redirect,get_object_or_404
from app import utilis
from app.users.decorators import login_required
from .models import Playlist
from app.watch_events.models import WatchEvent
from .schemas import playlistcreateshema
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

