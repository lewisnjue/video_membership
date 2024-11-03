from  app import config
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.exceptions import HTTPException
settings = config.get_settings()
from cassandra.cqlengine.query import (
    DoesNotExist,
    MultipleObjectsReturned
)
BASE_DIR = settings.base_dir

TEMPLATE_DIR = settings.template_dir

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def redirect(path,cookies:dict = {},remove_session=False):
    response = RedirectResponse(path,status_code=302)
    for k , v in cookies.items():
        response.set_cookie(key=k,value=v,httponly=True)
    if remove_session:

        response.set_cookie(key='session_ended',value=1,httponly=True)
        response.delete_cookie('session_id')


        
    return response


def render(request,template_name,context,cookies:dict = {}):
    ctx = context.copy()
    ctx.update({"request":request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str)
    if len(cookies.keys()) > 0:
        for k,v in cookies.items():
            response.set_cookie(key=k, value=v,httponly=True)
    
    return response


def get_object_or_404(classname,**kwargs):
    obj = None
    try :
        obj = classname.objects.get(**kwargs)
    except DoesNotExist:
        raise HTTPException(status_code=404)
    except MultipleObjectsReturned:
        raise HTTPException(status_code=400)

    except Exception:
        raise HTTPException(status_code=500)
    return obj
