from fastapi import FastAPI
from .api.debris_analysis_api import router
from . import setting
import uvicorn

app = FastAPI()

app.include_router(router)


def start() -> None:
    uvicorn.run("orbital_debris_analysis.main:app", host=setting.HOST, port=setting.PORT, reload=setting.DEBUG)
