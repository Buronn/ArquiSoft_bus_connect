from clients.Client import Client

print("Service: ", Client)
class Suma(Client):
    def __init__(self):
        print(f"""Cliente de suma
        Ingrese los números separados por un ' '.\n Para cerrar el programa escriba quit""")
        super().__init__("buron")
        
if __name__ == "__main__":
    keep_alive = True
    while(keep_alive):
        numbers = input("\ningrese los números: ")
        if numbers == 'quit':
            keep_alive = False
        else: 
            a = Suma()
            a.exec_client(debug=True, climsg=numbers)

    print("Cerrando cliente, hasta pronto ....")