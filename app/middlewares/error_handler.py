from typing import Union
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next) -> Union[Response, JSONResponse]:
        try:
            response = await call_next(request)
        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content={"error": str(exc)}
            )
        else:
            return response