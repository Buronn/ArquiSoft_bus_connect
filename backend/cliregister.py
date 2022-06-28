from clients.Client import Client
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Registro")
    keep_alive = True
    try:
        while(keep_alive):
            user = input("Ingrese usuario: ")
            password = getpass("Ingrese contraseña: ")
            email = input("Ingrese email: ")
            phone = input("Ingrese telefono: ")
            
            try: 
                climsg = {
                    "user": user,
                    "password": password,
                    "email": email,
                    "phone": phone
                }
                a = Client("bregi")
                msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                print("###################################\n\n", msg, "\n\n###################################")
            except Exception as e:
                print("Error: ", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()