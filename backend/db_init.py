from services.models import Usuario, Base
from sqlalchemy import create_engine
from services.config import Config
from services.models import Usuario, Base
from sqlalchemy.orm import Session
import datetime

def init_db():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
    session = Session(engine)
    if not session.query(Usuario).filter(Usuario.email == 'admin').first():
        usuario = Usuario(username='admin', password='admin', email='admin', phone='phone', fecha_ingreso=datetime.datetime.now())
        session.add(usuario)
    session.commit()
    session.close()
    return True
