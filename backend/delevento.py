from clients.Service import Service
from database.session import session
from database.models import Usuario, Miembro, Grupo, Evento, to_dict
import json, sys, os, jwt, datetime
from time import sleep

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
            eventos_del_usuario = db.query(Evento).filter_by(usuario_id=current_user.id).all()
            if climsg["grupo"] == "-1":
                for evento in eventos_del_usuario:
                    if evento.id == int(climsg["id"]):
                        db.delete(evento)
                        db.commit()
                        return "Evento eliminado"
                return "Evento no encontrado o no tienes permisos para eliminarlo"
            else:
                grupo = db.query(Grupo).filter_by(id=climsg["grupo"]).first()
                miembro = db.query(Miembro).filter_by(usuario_id=current_user.id,grupo_id=grupo.id).first()
                evento = db.query(Evento).filter_by(id=climsg["id"]).first()
                if evento.grupo_id == miembro.grupo_id:
                    if miembro.admin:
                        db.delete(evento)
                        db.commit()
                        return "Evento eliminado"
                return "No tienes permisos para eliminar este evento"
                    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error: " + str(e) + " " + fname + " " + str(exc_tb.tb_lineno)

def main():
    try:
        DelEvento()
    except Exception as e:
        print(e)
        sleep(30)
        main()

if __name__ == "__main__":
    main()

