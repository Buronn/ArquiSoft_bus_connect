from clients.Service import Service
from database.session import session
from database.models import Usuario, Miembro, Grupo, Evento, to_dict
import json, sys, os, jwt, datetime

class DelEvento(Service):
    def __init__(self):
        print("Servicio de eliminación de eventos")
        super().__init__("bdven")
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
            evento = climsg["id"]
            evento = db.query(Evento).filter_by(id=evento).first()
            if evento is None:
                return "Evento no encontrado"
            db.delete(evento)
            db.commit()
            return "Evento eliminado"
                    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error: " + str(e) + " " + fname + " " + str(exc_tb.tb_lineno)

if __name__ == "__main__":
    a = DelEvento()
