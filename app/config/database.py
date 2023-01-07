"""Database configuration."""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

sqlite_filename = "../../database.sqlite"
base_dir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(base_dir, sqlite_filename)}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
