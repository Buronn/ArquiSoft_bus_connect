from clients.Service import Service
from database.session import session
from database.models import Usuario, Miembro, Grupo
import json, sys, os, jwt, datetime

class Grupos(Service):
    def __init__(self):
        print("Servicio de grupos de usuarios")
        super().__init__("bgrup")
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
            if current_user is None:
                return "Usuario no encontrado"
            if db.query(Grupo).filter_by(nombre=climsg["titulo"]).first() is not None:
                return "Grupo ya existe"
            else:
                grupo = Grupo(
                    nombre=climsg["titulo"],
                    descripcion=climsg["descripcion"],
                )
                
               
                db.add(grupo)
                miembro_admin = Miembro(
                    usuario=current_user,
                    rol="admin",
                    admin=True,
                    join_date=datetime.datetime.now(),
                    grupo=grupo
                ) 
                db.add(miembro_admin)
                db.commit()
                for email in climsg["emails"].split(","):
                    usuario = db.query(Usuario).filter_by(email=email).first()
                    if usuario is None:
                        return "Usuario no encontrado"
                    else:
                        miembro = Miembro(
                            usuario=usuario,
                            rol="miembro",
                            admin=False,
                            join_date=datetime.datetime.now(),
                            grupo=grupo
                        )
                        db.add(miembro)
                        db.commit()
                return "Grupo creado con id: " + str(grupo.id)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error: " + str(e) + " " + fname + " " + str(exc_tb.tb_lineno)
        finally:
            db.close()
            return "Error"

if __name__ == "__main__":
    a = Grupos()
