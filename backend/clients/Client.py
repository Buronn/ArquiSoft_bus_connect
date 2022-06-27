from socket import socket, AF_INET, SOCK_STREAM
import os

class Client:
    '''Sirve como base para cualquier instancia cliente que quiera utilizar algun servicio'''
    def __init__(self, name):
        self.s = socket(AF_INET, SOCK_STREAM)

        # Revisar si el nombre cumple largo maximo.
        if len(name) != 5:
            raise ValueError("Max length of service name is 5")
        self.name = name

    def exec_client(self, endpoint=(os.environ["SOCKET_HOST"],int(os.environ["BUS_PORT"])), climsg="", debug=False):
        '''Genera la conexión con el BUS y consume el servicio especificado'''
        def safe_recv(socket, length):
            '''Se utiliza para evitar errores al trabajar con el socket'''
            res = socket.recv(length)

            if res == b'' and length != 0:
                # En caso que se caiga el tunel SSH o el BUS
                raise ConnectionError("Se ha cerrado la conexion con el BUS inesperadamente")
            elif len(res) != length:
                # No va a ocurrir nunca pq el BUS arregla los largos.
                raise Exception("largo recibido es inconsistente")

            return res
            
        def check_service(name):
            getsv = b"00005getsv"

            self.s.send(getsv)
            
            length = safe_recv(self.s,5)
            print('len: ', length)
            nop    = safe_recv(self.s,5)
            print('nop', nop) 
            msg    = safe_recv(self.s,int(length)-5)
            print('msg', msg)

            if name.encode() not in msg:
                print("Service not found")
                
                raise ConnectionError
    
        
        try:
            # Iniciamos la conección con el BUS.
            self.s.connect(endpoint)
            
            # Revisamos que el servicio este disponible.
            check_service(self.name)
        except Exception as e:
            print(e)
            return
        
        # Enviamos el mensaje
        msg_len = str( len(climsg) + 5 )
        data = ("0"*(5 - len(msg_len)%5) + msg_len + self.name + climsg).encode()
        self.s.send(data)

        # Consumimos y parseamos los campos del socket
        try:
            length = safe_recv(self.s,5)
            srvice = safe_recv(self.s,5)
            code   = safe_recv(self.s,2)
            srvmsg = safe_recv(self.s,int(length)-7)
        except ValueError as e:
            # Informamos del error del formato sin terminar el programa.
            print(e)
            return
        print("\n2",length, srvice, code, srvmsg)
        self.s.close()
        return srvmsg.decode()