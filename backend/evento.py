from clients.Service import Service
from database.session import session
from database.models import Usuario, Miembro, Grupo, Evento, to_dict
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
            duracion = int(climsg["duracion"])
            grupo = climsg["grupo"]
            eventos = []
            if grupo == "-1":
                grupo = None
                eventoss = db.query(Evento).filter_by(usuario_id=current_user.id).all()
                for evento in eventoss:
                    eventos.append(to_dict(evento))
                membresia = db.query(Miembro).filter_by(usuario_id=current_user.id).all()
                for miembro_grupo in membresia:
                    eventoss = db.query(Evento).filter_by(grupo_id=miembro_grupo.grupo_id).all()
                    for evento in eventoss:
                        eventos.append(to_dict(evento))

            else:
                grupo = db.query(Grupo).filter_by(id=grupo).first()
                eventos = []
                eventoss = db.query(Evento).filter_by(grupo_id=grupo.id).all()
                for evento in eventoss:
                    eventos.append(to_dict(evento))
                miembros = db.query(Miembro).filter_by(grupo_id=grupo.id).all()
                for miembro in miembros:
                    eventoss = db.query(Evento).filter_by(usuario_id=miembro.usuario_id).all()
                    for evento in eventoss:
                        eventos.append(to_dict(evento))
            if db.query(Evento).filter_by(nombre=titulo).first() is not None:
                return "Evento ya existe"
            inicio_laboral = 8
            fin_laboral = 22
            bloques_usados = []
            for evento in eventos:
                # dia del evento en formato DayOfWeek
                print("evento: " + str(evento))
                dia = evento["fecha_inicio"].split("-")[0]
                inicio = int(evento["fecha_inicio"].split("-")[1].split(":")[0])
                fin = int(evento["fecha_fin"].split("-")[1].split(":")[0])
                d = str(dia)+"-"+str(inicio)+"-"+str(fin)
                print(d)
                bloques_usados.append(d)
            dias = ["monday", "tuesday", "wednesday", "thursday", "friday"]
            for dia in dias:
                for hora in range(inicio_laboral, fin_laboral):
                    ocupado = False
                    for bloque in bloques_usados:
                        if dia == bloque.split("-")[0]:
                            actual = hora
                            inicio_bloque = int(bloque.split("-")[1])
                            fin_bloque = int(bloque.split("-")[2])
                            if actual >= inicio_bloque and actual < fin_bloque:
                                ocupado = True
                                hora = int(bloque.split("-")[1])
                                break
                    if ocupado:
                        continue
                    # formato de fecha: DayOfWeek-Hora
                    fecha_inicio = dia+"-"+str(hora)+":00"
                    fecha_fin = dia+"-"+str(hora+duracion)+":00"
                    if hora+duracion > fin_laboral:
                        continue
                    evento = Evento(
                        nombre=titulo,
                        descripcion=descripcion,
                        usuario_id=current_user.id,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        grupo_id = None
                    )
                    if grupo:
                        evento.grupo_id = grupo.id
                    print("user id:", current_user.id, fecha_inicio, fecha_fin)
                    db.add(evento)
                    db.commit()
                    return "Evento creado"
            else:
                return "No hay bloques disponibles"
                    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error: " + str(e) + " " + fname + " " + str(exc_tb.tb_lineno)

if __name__ == "__main__":
    a = Eventos()
