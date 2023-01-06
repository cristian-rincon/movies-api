from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.auth import generate_token
from app.routers.v1.models import BaseUser

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
)


@router.post("/login")
def login(user: BaseUser):
    mock_user = BaseUser(username="admin", password="admin")
    if user == mock_user:
        token = generate_token({"username": user.username})
        return JSONResponse(content={"token": token}, status_code=200)
    return JSONResponse(content={"error": "Invalid credentials"}, status_code=401)
