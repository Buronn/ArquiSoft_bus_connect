from clients.Service import Service
from database.session import session
from database.models import Usuario
import datetime

class Registro(Service):
    def __init__(self):
        print("Servicio de registro de usuarios")
        super().__init__("bregi")
        self.start_service(debug=True)
    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        print("Que wea: ", climsg)
        #return "Funciona pinche servicio " + climsg
        db = session()
        user,password,email,phone = climsg.split(" ")
        if not db.query(Usuario).filter(Usuario.email == email).first():
            usuario = Usuario(username=user, password=password, email=email, phone=phone, fecha_ingreso=datetime.datetime.now())
            db.add(usuario)
            db.commit()
            db.close()
            return "Usuario registrado"
        else:
            db.close()
            return "Usuario ya existe"

if __name__ == "__main__":
    a = Registro()