from db_init import init_db
from clients.Service import Service

class Suma(Service):
    def __init__(self):
        print("Servicio de suma de enteros")
        super().__init__("buron")
        self.start_service(debug=True)
    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        print("Que wea: ", climsg)
        #return "Funciona pinche servicio " + climsg
        numbers = [int(i) for i in climsg.split(" ")]
        suma = sum(numbers)
        response = str(suma)
        return response


if __name__ == "__main__":
    init_db()
    a = Suma()