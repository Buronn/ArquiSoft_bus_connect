from clients.Service import Service
from database.session import session
from database.models import Usuario, Miembro, Grupo, Evento, to_dict
import json, sys, os, jwt, datetime
from time import sleep

class VerEvento(Service):
    def __init__(self):
        print("Servicio para ver eventos")
        super().__init__("bvven")
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
            eventos = []
            my_events = db.query(Evento).filter_by(usuario_id=current_user.id,grupo_id=None).all()
            for event in my_events:
                eventos.append(to_dict(event))
            membresia = db.query(Miembro).filter_by(usuario_id=current_user.id).all()
            for miembro_grupo in membresia:
                my_events = db.query(Evento).filter_by(grupo_id=miembro_grupo.grupo_id).all()
                for event in my_events:
                    eventos.append(to_dict(event))
            if eventos:
                output = "----------------------------------------------------\n"
                for event in eventos:
                    output += "ID: "+str(event["id"])+"\n"
                    output += "Nombre: "+event["nombre"]+"\n"
                    output += "Descripcion: "+event["descripcion"]+"\n"
                    output += "Fecha inicio: "+event["fecha_inicio"]+"\n"
                    output += "Fecha fin: "+event["fecha_fin"]+"\n"
                    try:
                        output += "Grupo: "+str(event["grupo_id"])+" ("+db.query(Grupo).filter_by(id=event["grupo_id"]).first().nombre+")\n"
                    except:
                        output += "Grupo: Personal\n"
                    output += "Creador: "+str(event["usuario_id"])+" ("+db.query(Usuario).filter_by(id=event["usuario_id"]).first().email+")\n"
                    output += "----------------------------------------------------\n"
                # replace 0xde 
                output = output.replace("\xde", "")
                return (output)
            else:
                return "No hay eventos"
                    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error: " + str(e) + " " + fname + " " + str(exc_tb.tb_lineno)

def main():
    try:
        VerEvento()
    except Exception as e:
        print(e)
        sleep(30)
        main()

if __name__ == "__main__":
    main()

