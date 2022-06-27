from clients.Service import Service
from database.session import session
from database.models import Usuario
import bcrypt
import os
import jwt
import datetime


class Registro(Service):
    def __init__(self):
        print("Servicio de registro de usuarios")
        super().__init__("bregi")
        self.start_service(debug=True)

    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        print("Que wea: ", climsg)
        # return "Funciona pinche servicio " + climsg
        db = session()
        user, password, email, phone = climsg.split(" ")
        try:
            if not db.query(Usuario).filter(Usuario.email == email).first():
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                usuario = Usuario(username=user, password=hashed_password.decode(
                    'utf-8'), email=email, phone=phone, fecha_ingreso=datetime.datetime.now())
                db.add(usuario)
                db.commit()
                db.close()
                usuario = db.query(Usuario).filter(Usuario.email == email).first()
                token = jwt.encode({
                    'id': usuario.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                    os.environ['SECRET_KEY'])
                return token
            else:
                db.close()
                return "Usuario ya existe"
        except Exception as e:
            db.close()
            return str(e)

if __name__ == "__main__":
    a = Registro()
