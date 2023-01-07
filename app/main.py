"""Main module for the FastAPI app."""

from fastapi import FastAPI

from app.config.database import Base, engine
from app.routers.v1.auth import router as auth_router
from app.routers.v1.movies import router as movies_router

# from app.middlewares.error_handler import ErrorHandlerMiddleware

ROUTERS = [movies_router, auth_router]


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


@api.get("/ping")
def ping() -> str:
    """Ping endpoint. Just for testing purposes."""
    return "pong!"
