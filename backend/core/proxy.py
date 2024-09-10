# global_request is a context variable that binds to the current request object.
from contextvars import ContextVar
from fastapi import Request

def bind_contextvar(contextvar):
    class ContextVarBind:
        __slots__ = ()

        def __getattr__(self, name):
            return getattr(contextvar.get(), name)

        def __setattr__(self, name, value):
            setattr(contextvar.get(), name, value)

        def __delattr__(self, name):
            delattr(contextvar.get(), name)

        def __getitem__(self, index):
            return contextvar.get()[index]

        def __setitem__(self, index, value):
            contextvar.get()[index] = value

        def __delitem__(self, index):
            del contextvar.get()[index]

    return ContextVarBind()


request_var: ContextVar[Request] = ContextVar("request")
global_request:Request = bind_contextvar(request_var)
"""
global request object
"""


async def bind_context_request(request: Request, call_next):
    """
    middleware for request
    bind the current request to context var
    example:
    app = FastAPI()
    app.middleware("http")(bind_context_request)
    """
    token = request_var.set(request)
    try:
        response = await call_next(request)
        return response
    finally:
        request_var.reset(token)