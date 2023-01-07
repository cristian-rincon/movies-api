"""Auth router."""
import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.middlewares.auth import generate_token
from app.schemas.user import BaseUser

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
)


@router.post("/login")
def login(user: BaseUser) -> JSONResponse:
    """Login endpoint."""
    mock_user = BaseUser(username=os.getenv("ADMIN_USER", "admin"), password=os.getenv("ADMIN_PASS", "123456"))
    if user == mock_user:
        token = generate_token({"username": user.username})
        return JSONResponse(content={"token": token}, status_code=200)
    return JSONResponse(content={"error": "Invalid credentials"}, status_code=401)
