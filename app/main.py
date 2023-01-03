from fastapi import FastAPI

from app.routers.v1.movies import router


api = FastAPI(
    title="Movies API",
    description="A simple API to learn FastAPI",
    version="0.1.0",

)

api.include_router(router)

@api.get("/ping")
def ping():
    return "pong!"