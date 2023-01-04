from fastapi import FastAPI

from app.routers.v1.movies import router as movies_router
from app.routers.v1.auth import router as auth_router


api = FastAPI(
    title="Movies API",
    description="A simple API to learn FastAPI",
    version="0.1.0",

)

api.include_router(movies_router)
api.include_router(auth_router)

@api.get("/ping")
def ping():
    return "pong!"