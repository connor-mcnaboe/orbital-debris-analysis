from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.debris_analysis_api import router
from . import setting
import uvicorn

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

def start() -> None:
    uvicorn.run("orbital_debris_analysis.main:app", host=setting.HOST, port=setting.PORT, reload=setting.DEBUG)
