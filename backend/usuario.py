from clients.Service import Service
from database.session import session
from database.models import Usuario, Miembro, Grupo, Evento, to_dict
import json, sys, os, jwt, datetime
from time import sleep

class Usuarios(Service):
    def __init__(self):
        print("Servicio para ver usuarios")
        super().__init__("buser")
        self.start_service(debug=True)

    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        db = session()
        try:
            climsg = json.loads(climsg)
            token = climsg["token"]
            decoded = jwt.decode(
                token, os.environ['SECRET_KEY'], algorithms=['HS256'])
            current_user = db.query(Usuario).filter_by(id=decoded['id']).first()
            usuarios = []
            for user in db.query(Usuario).all():
                usuarios.append(to_dict(user))
            if usuarios:
                output = "----------------------------------------------------\n"
                for usuario in usuarios:
                    output += "ID: "+str(usuario["id"])+"\n"
                    output += "Nombre: "+usuario["username"]+"\n"
                    output += "Email: "+usuario["email"]+"\n"
                    output += "Telefono: "+usuario["phone"]+"\n"
                    output += "----------------------------------------------------\n"
                # replace 0xde 
                output = output.replace("\xde", "")
                return (output)
            else:
                return "No hay usuarios"
                    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error: " + str(e) + " " + fname + " " + str(exc_tb.tb_lineno)

def main():
    try:
        Usuarios()
    except Exception as e:
        print(e)
        sleep(30)
        main()

if __name__ == "__main__":
    main()

