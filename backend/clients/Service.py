from socket import socket, AF_INET, SOCK_STREAM
import os

class Service:
    '''Sirve como la base para cualquier servicio que se quiera implementar.
    Solo se debe utilizar herencia y reimplementar la funcion `service_function`'''
    def __init__(self,name):
        self.s = socket(AF_INET, SOCK_STREAM)
        
        # Revisar si el nombre cumple largo maximo.
        if len(name) > 5:
            raise ValueError("Max length of service name is 5")
        self.name = "0"*(5-len(name)) + name
        

    def __del__(self):
        self.s.close()

    def start_service(self, endpoint=(os.environ["SOCKET_HOST"],5000), debug=False):
        '''Genera la conexion con el BUS y genera un loop donde se recibiran y procesaran los mensajes'''
        
        def safe_recv(socket, length):
            '''Se utiliza para evitar errores al trabajar con el socket'''
            res = socket.recv(length)

            if res == b'' and length != 0:
                # En caso que se caiga el tunel SSH o el BUS
                raise ConnectionError("Se ha cerrado la conexion con el BUS inesperadamente")
            elif len(res) != length:
                # No va a ocurrir nunca pq el BUS arregla los largos.
                raise Exception("largo recivido es inconsistente")

            return res

        def send_sinit(name):
            len_str = str(len(name) + 5)
            sinit = "0"*(5 - len(len_str)%5) + len_str + "sinit" + name
            
            self.s.send(sinit.encode())
            msg = safe_recv(self.s,17)

            if msg[5:7] == b'NK':
                raise ConnectionError

        # Iniciamos la coneccion con el BUS.
        self.s.connect(endpoint)

        # Iniciamos el servicio
        
        try:
            send_sinit(self.name)
        except Exception as e:
            print(e)
            return

        # Recibiremos requests por siempre
        while(1):
            # Consumimos y parseamos los campos del socket
            try:
                length = safe_recv(self.s,5)
                srvice = safe_recv(self.s,5)
                climsg = safe_recv(self.s,int(length)-5)
            except ValueError as e:
                # Informamos del error del formato sin terminar el programa.
                self.s.send(b"00008"+self.name.encode()+b"400")
                print(e)

                continue
            
            # Validamos que el servicio especificado sea el este
            if srvice.decode() != self.name and srvice.decode() != "sinit":
                self.s.send(b"00008"+self.name.encode()+b"501")
                continue
            
            if debug:
                print(length, srvice, climsg)
            
            # Ejecutamos la función especifica del servicio
            res = self.service_function(climsg.decode())
     
            # Enviamos la respuesta al cliente
            length = str(len(res) + 5)
            srvmsg = "0"*(5 - len(length)%5) + length + self.name + res
            self.s.send(srvmsg.encode())

        self.s.close()

    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        print(climsg)
        return "ack"