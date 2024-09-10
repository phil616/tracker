import asyncio
from http import HTTPStatus
import traceback
from fastapi import Request
from response.std import create_response


def get_http_status_description(status_code: int) -> str:
    """
    Returns the description of the HTTP status code.
    If the status code is not recognized, returns "Unknown Status Code".

    :param status_code: HTTP status code
    :return: Description of the HTTP status code
    """
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "Unknown Status Code"


async def database_exception_handler(req: Request, exc: Exception):
    """
    Handles database exceptions.

    :param req: Request object
    :param exc: Exception object
    :return: JSON response with error details
    """
    stack_trace = traceback.format_exc()
    headers=exc.headers
    error_response = {
        "error": "Database Error",
        "detail": "An error occurred while accessing the database",
    }
    if req.app.debug:
        error_response.update({"stack_trace": stack_trace})
    return create_response(data=error_response, status=500,message="ERROR",headers=headers)



async def global_exception_handler(req: Request, exc: Exception):
    """
    Handles all other exceptions.

    :param req: Request object
    :param exc: Exception object
    :return: JSON response with error details
    """
    # ignore asyncio.exceptions.CancelledError  allow Ctrl + C to stop the server
    if isinstance(exc, asyncio.exceptions.CancelledError):
        return None

    stack_trace = traceback.format_exc()
    headers=exc.headers
    error_response = {
        "error": get_http_status_description(exc.status_code),
        "detail": exc.detail,
    }
    if req.app.debug:
        error_response.update({"stack_trace": stack_trace})
    return create_response(data=error_response, status=exc.status_code,message="ERROR",headers=headers)

