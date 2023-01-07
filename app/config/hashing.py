from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt(password: str):
    return pwd_ctx.hash(password)

def verify(plain_password, hashed_password):
    return pwd_ctx.verify(plain_password, hashed_password)