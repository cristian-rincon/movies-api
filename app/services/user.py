from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import hashing
from app.models.user import User as UserORM
from app.schemas.user import User as UserSchema



def create(request: UserSchema, db: Session):

    new_user = UserORM(
        name=request.name,
        email=request.email,
        password=hashing.bcrypt(request.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_one(id: int, db: Session):
    if user := db.query(UserORM).filter(UserORM.id == id).first():
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not found.",
        )


def bulk_load(data, db: Session):
    for i in data:
        new_user = UserORM(
            name=i[0], email=i[1], password=hashing.Hash.bcrypt(i[2])
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return len(data)
