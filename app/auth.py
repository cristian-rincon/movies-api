from jwt import encode, decode
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

def generate_token(data: dict):
    return encode(payload = data, key = "secret", algorithm = "HS256")

def verify_token(token: str):
    return decode(jwt = token, key = "secret", algorithms = ["HS256"])


class JWTBearer(HTTPBearer):

    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = verify_token(auth.credentials)
        if data['username'] != 'admin':
            raise HTTPException(status_code=401, detail="Invalid username")

        
