from sqlalchemy import create_engine
from .config import Config
from sqlalchemy.orm import Session

def session():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    session = Session(engine)
    return session
