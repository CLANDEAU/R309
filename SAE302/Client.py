import socket
import threading
import subprocess

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
                self.__client_socket.send(message.encode())
            else:
                self.__client_socket.send(message.encode())
                data = self.__client_socket.recv(32000).decode()
                if data == "disconnect":
                    com = False
                elif data == "ping 192.157.65.78":
                    print("Voici le résultat de la commmande ping 192.157.65.78:")
                    subprocess.Popen('ping 192.157.65.78')
                else:
                    print(data)


socket1=Socket()
echange = threading.Thread(target=socket1.echange)
echange.start()
echange.join()
