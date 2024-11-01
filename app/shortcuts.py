from  app import config
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
settings = config.get_settings()

BASE_DIR = settings.base_dir

TEMPLATE_DIR = settings.template_dir

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def redirect(path,cookies:dict = {}):
    response = RedirectResponse(path,status_code=302)
    for k , v in cookies.items():
        response.set_cookie(key=k,value=v,httponly=True)
        
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


