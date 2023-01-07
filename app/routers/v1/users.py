import csv
from io import StringIO

from fastapi import APIRouter, Depends, File
from sqlalchemy.orm import Session

from app.config import database, oauth2
from app.schemas import user as user_schema
from app.services import user as user_service

router = APIRouter(tags=['users'], prefix='/user')
get_db = database.get_db


@router.post('', response_model=user_schema.UserResponse)
def create_user(request: user_schema.User, db: Session = Depends(get_db)):
    return user_service.create(request, db)


@router.get('/{id}', response_model=user_schema.UserResponse)
def get_user(id, db: Session = Depends(get_db)):
    return user_service.get_one(id, db)


@router.post('/bulk')
def bulk_load_users(incoming_file: bytes = File(...),
                    db: Session = Depends(get_db),
                    current_user: user_schema.User = Depends(
                        oauth2.get_current_user)):

    content = incoming_file.decode()
    incoming_file = StringIO(content)
    reader = csv.reader(incoming_file, delimiter=",")
    header = next(reader)
    data = []
    if header is not None:
        data.extend(tuple(row) for row in reader)
    user_service.bulk_load(data, db)
    return f'{len(data)} users loaded'
