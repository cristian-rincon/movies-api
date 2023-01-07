"""Main module for the FastAPI app."""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config.database import Base, engine
from app.routers.v1.auth import router as auth_router
from app.routers.v1.movies import router as movies_router
from app.routers.v1.users import router as users_router


ROUTERS = [users_router, auth_router, movies_router]


def create_api() -> FastAPI:
    """Create the FastAPI app."""
    app = FastAPI(
        title="Movies API",
        description="A simple API to learn FastAPI",
        version="0.1.0",
    )
    # Just for testing purposes
    # api.add_middleware(ErrorHandlerMiddleware)

    for router in ROUTERS:
        app.include_router(router)
    return app


api = create_api()

Base.metadata.create_all(bind=engine)


@api.get("/")
def index() -> str:
    """This endpoint will redirect response to /docs."""
    return RedirectResponse("/docs")


@api.get("/ping")
def ping() -> str:
    """Ping endpoint. Just for testing purposes."""
    return "pong!"
