from fastapi import FastAPI

from app.config.database import Base, engine
from app.routers.v1.auth import router as auth_router
from app.routers.v1.movies import router as movies_router

ROUTERS = [movies_router, auth_router]


def create_api():
    api = FastAPI(
        title="Movies API",
        description="A simple API to learn FastAPI",
        version="0.1.0",
    )

    for router in ROUTERS:
        api.include_router(router)
    return api


api = create_api()

Base.metadata.create_all(bind=engine)


@api.get("/ping")
def ping():
    return "pong!"
