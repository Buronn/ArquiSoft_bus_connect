from clients.Client import Client
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Borrar Evento")
    keep_alive = True
    try:
        while(keep_alive):
            token = getpass("Token: ")
            id = input("ID del Evento: ")
            grupo = input("ID del Grupo (\"-1\" para evento individual): ")
            try: 
                a = Client("bdven")
                climsg = {
                    "token": token,
                    "id": id,
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