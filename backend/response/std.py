from typing import Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi.responses import JSONResponse
from functools import wraps

def generate_timestamp():
    """
    Generates a timestamp in the format of "YYYY-MM-DD HH:MM:SS"
    """
    return datetime.now().isoformat()


class GenericResponse(BaseModel):
    """
    A generic response model that can be used to return any type of data from a request.
    The Response looks like this:
    {
        "status": 200,
        "message": "SUCCESS",
        "data": "Some data",
        "timestamp": "2021-08-17T12:34:56.789Z"
    }
    """
    status: int = Field(200, description="The HTTP status code of the response")
    message: str = Field(default="SUCCESS", description="A message describing the result of the request")
    data: Optional[Any] = Field(None, description="The data returned by the request")
    timestamp: str = Field(...,default_factory=generate_timestamp, description="The timestamp of the response")



def create_response(status: int = 200, data: Any = None, message: str = "SUCCESS",headers:dict={}):
    """
    A helper function to create a JSONResponse object with the given status, data, and message.

    If the data is not JSON serializable, it will be returned as is.
    """
    try:
        json_response = JSONResponse(
                content=GenericResponse(status=status, data=data, message=message).model_dump(),
                status_code=status,
                headers=headers
        )
        return json_response
    except Exception:
        return data


def unified_response(func):
    """
    the unified_response decorator is used to wrap the endpoint functions and convert the original response to a JSONResponse object.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        original_response = await func(*args, **kwargs)
        return create_response(data=original_response)
    return wrapper

class URFRouter(APIRouter):
    """
    Unified Response Formatted Router is a custom router that automatically wraps the endpoint functions with the unified_response decorator.

    Example usage:
    ```
    router = URFRouter()

    @router.get("/users")
    async def get_users():
        return {"users": ["user1", "user2"]}

    app.include_router(router)
    ```
    """
    def add_api_route(self, path, endpoint, **kwargs):
        decorated_endpoint = unified_response(endpoint)
        super().add_api_route(path, decorated_endpoint, **kwargs)

