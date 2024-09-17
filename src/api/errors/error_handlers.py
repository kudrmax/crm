from fastapi import Request
from fastapi.responses import JSONResponse

from src.errors import *


def contact_already_exists_exception_handler(request: Request, exc: ContactAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={"message": f"Contact with name {exc.name} already exists"},
    )


def item_not_found_exception_handler(request: Request, exc: ContactNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Contact with name {exc.name} not found"},
    )
