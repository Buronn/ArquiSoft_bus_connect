from clients.Client import Client
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Grupo")
    keep_alive = True
    try:
        while(keep_alive):
            token = getpass("Token: ")
            titulo = input("Titulo: ")
            descripcion = input("Descripcion: ")
            emails = input("Ingrese los emails de los usuarios separados por comas: ")
            try: 
                a = Client("bgrup")
                climsg = {
                    "token": token,
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "emails": emails
                }
                msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                print("###################################\n\n", msg, "\n\n###################################")
            except Exception as e:
                print("Error: ", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()