
def all_exception():
    from starlette.exceptions import HTTPException as Starlette 
    from app.shortcuts import  render, redirect
    from app.users.exceptions import LoginRequiredException

    from  .main import app
    @app.exception_handler(LoginRequiredException)
    async def login_required_exception_handler(request,exc):
        return redirect(f'/login?next={request.url}',remove_session=True)

    @app.exception_handler(Starlette)
    async def general_exception_handler(request,exc):
        status_code = exc.status_code 
        template_name = 'errors/main.html'
        if status_code == 404:
            template_name = 'errors/404.html'

        context = {"status_code":status_code}
        return render(request=request,template_name=template_name,context=context)



exceptions_all = all_exception()


