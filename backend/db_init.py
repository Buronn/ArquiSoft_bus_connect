from database.models import Usuario, Base
from sqlalchemy import create_engine
from database.config import Config
from database.models import Usuario, Base
from sqlalchemy.orm import Session
import datetime, bcrypt,os

def init_db():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
    session = Session(engine)
    if not session.query(Usuario).filter(Usuario.email == os.environ["ADMIN_ACCOUNT"]).first():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(os.environ["ADMIN_PASSWORD"].encode('utf-8'), salt)
        usuario = Usuario(username='admin', password=hashed_password ,email=os.environ["ADMIN_ACCOUNT"], phone='000', fecha_ingreso=datetime.datetime.now())
        session.add(usuario)
    session.commit()
    session.close()
    return True

init_db()
