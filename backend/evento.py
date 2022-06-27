from clients.Service import Service
from database.session import session
from database.models import Usuario, Miembro, Grupo, Evento
import json, sys, os, jwt, datetime

class Eventos(Service):
    def __init__(self):
        print("Servicio de eventos de grupos")
        super().__init__("beven")
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
            titulo = climsg["titulo"]
            descripcion = climsg["descripcion"]
            duracion = climsg["duracion"]
            grupo = climsg["grupo"]
            grupo = db.query(Grupo).filter_by(id=grupo).first()
            if grupo is None:
                return "Grupo no encontrado"
            if db.query(Evento).filter_by(nombre=titulo).first() is not None:
                return "Evento ya existe"
            dias = {
                "lunes": [],
                "martes": [],
                "miercoles": [],
                "jueves": [],
                "viernes": [],
            }
            miembros = db.query(Miembro).filter_by(grupo=grupo).all()
            for miembro in miembros:
                eventos = db.query(Evento).filter_by(usuario_id=miembro.usuario_id).all()
                for evento in eventos:
                    print(evento.fecha_inicio)
                    print(evento.fecha_fin)
                
            return "lol lol lol"
                    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error: " + str(e) + " " + fname + " " + str(exc_tb.tb_lineno)

if __name__ == "__main__":
    a = Eventos()
