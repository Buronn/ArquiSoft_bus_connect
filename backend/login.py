from clients.Service import Service
from database.session import session
from database.models import Usuario
import bcrypt
import os
import jwt
import datetime


class Login(Service):
    def __init__(self):
        print("Servicio de login de usuarios")
        super().__init__("blogi")
        self.start_service(debug=True)

    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        db = session()
        email, password = climsg.split(" ")
        user = db.query(Usuario).filter(Usuario.email == email).first()
        try:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                    os.environ['SECRET_KEY'])
                return token
            else:
                db.close()
                return "Contraseña incorrecta"
        except Exception as e:
            db.close()
            return str(e)


if __name__ == "__main__":
    a = Login()
