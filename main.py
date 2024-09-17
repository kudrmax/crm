import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.api.errors.error_handlers import *
from src.api.errors.errors_global import global_exception_handler
from src.api.routers import router
from src.settings import settings

app = FastAPI(
    title=settings.app.title,
    description=settings.app.description,
    version=settings.app.version,
)
app.include_router(router)

logging.basicConfig(level=logging.ERROR)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(ContactNotFoundError, item_not_found_exception_handler)
app.add_exception_handler(ContactAlreadyExistsError, contact_already_exists_exception_handler)


@app.get("/")
def root():
    return RedirectResponse('/docs')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.server.host,
        port=settings.server.port,
        reload=True
    )
