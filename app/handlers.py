from starlette.exceptions import HTTPException
from app.shortcuts import    render
from app.main import app

@app.exception_handler(HTTPException)
async def http_exception_handler(request,exc):
    status_code = exc.status_code 
    template_name = 'errors/main.html'
    context = {"status_code":status_code}
    return render(request=request,template_name=template_name,context=context)
