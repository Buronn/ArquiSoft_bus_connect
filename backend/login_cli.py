from clients.Client import Client
from getpass import getpass
        
if __name__ == "__main__":
    print("Service: Login")
    keep_alive = True
    try:
        while(keep_alive):
            email = input("Ingrese email: ")
            password = getpass("Ingrese contraseña: ")

            try: 
                a = Client("blogi")
                climsg = email + " " + password
                msg = a.exec_client(debug=True, climsg=climsg)
                print("###################################\n\n", msg, "\n\n###################################")
            except Exception as e:
                print("Error: ", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()