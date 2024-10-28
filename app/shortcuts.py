from  app import config
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
settings = config.get_settings()

BASE_DIR = settings.base_dir

TEMPLATE_DIR = settings.template_dir

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def render(request,template_name,context):
    ctx = context.copy()
    ctx.update({"request":request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str)
    return response
    #return templates.TemplateResponse(template_name,ctx)
