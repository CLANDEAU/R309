import socket
import threading

class Socket:
    def __init__(self,host="127.0.0.1",port=8000):
        self.__host=host
        self.__port = port
        self.__client_socket = socket.socket()
        self.__client_socket.connect((host, port))

    def echange(self):
        com = True
        while com:
            message = input("Message envoyé=")
            if message == "disconnect":
                com = False
                self.__client_socket.send(message.encode())
            elif message == "kill":
                com = False
                self.__client_socket.send(message.encode())
            elif message == "reset":
                print("pas encore en action")
            else:
                self.__client_socket.send(message.encode())
                data = self.__client_socket.recv(1024).decode()
                if data == "disconnect":
                    com = False
                else:
                    print(data)


socket1=Socket()
echange = threading.Thread(target=socket1.echange)
echange.start()
echange.join()
