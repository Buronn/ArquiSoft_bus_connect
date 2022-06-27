from clients.Client import Client
from getpass import getpass
        
if __name__ == "__main__":
    print("Service: Registro")
    keep_alive = True
    while(keep_alive):
        user = input("Ingrese usuario: ")
        password = getpass("Ingrese contraseña: ")
        email = input("Ingrese email: ")
        phone = input("Ingrese telefono: ")

        try: 
            a = Client("bregi")
            climsg = user + " " + password + " " + email + " " + phone
            msg = a.exec_client(debug=True, climsg=climsg)
            print("###################################\n\n", msg, "\n\n###################################")
        except Exception as e:
            print("Error: ", e)


    print("Cerrando cliente, hasta pronto ....")