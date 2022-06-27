from clients.Client import Client
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Crear Evento")
    keep_alive = True
    try:
        while(keep_alive):
            token = getpass("Token: ")
            duracion = input("Cuanto durara tu evento (horas): ")
            titulo = input("Titulo: ")
            descripcion = input("Descripcion: ")
            grupo = input("ID del Grupo (\"-1\" para evento individual): ")
            try: 
                a = Client("beven")
                climsg = {
                    "token": token,
                    "duracion": duracion,
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "grupo": grupo
                }
                msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                print("###################################\n\n", msg, "\n\n###################################")
            except Exception as e:
                print("Error: ", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()