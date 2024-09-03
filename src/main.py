import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.api import router

app = FastAPI(title='CRMz')
app.include_router(router)


@app.get("/")
def root():
    return RedirectResponse('/docs')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
