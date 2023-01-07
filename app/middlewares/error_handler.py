"""Error handler middleware."""

from typing import Any, Union
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from fastapi.responses import JSONResponse


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Error handler middleware Class."""

    async def dispatch(
        self, request: Request, call_next: Any
    ) -> Union[Response, JSONResponse]:
        """Dispatch method."""
        try:
            response = await call_next(request)
        except Exception as exc:
            return JSONResponse(status_code=500, content={"error": str(exc)})
        else:
            return response
