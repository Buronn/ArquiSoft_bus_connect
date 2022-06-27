from clients.Client import Client
from getpass import getpass

print("Service: ", Client)
class Registro(Client):
    def __init__(self):
        super().__init__("bregi")
        
if __name__ == "__main__":
    print("Service: Registro")
    keep_alive = True
    while(keep_alive):
        user = input("Ingrese usuario: ")
        password = getpass("Ingrese contraseña: ")
        email = input("Ingrese email: ")
        phone = input("Ingrese telefono: ")

        try: 
            a = Registro()
            climsg = user + " " + password + " " + email + " " + phone
            a.exec_client(debug=True, climsg=climsg)
        except Exception as e:
            print("Error: ", e)


    print("Cerrando cliente, hasta pronto ....")