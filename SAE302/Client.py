import socket
import threading
host="127.0.0.1"
port= 8000
client_socket = socket.socket()
client_socket.connect((host, port))
def echange():
    com = True
    while com:
        message = input("Message envoyé= ")
        if message == "disconnect":
            com = False
            client_socket.send(message.encode())
        elif message == "reset":
            com = False
            client_socket.send(message.encode())
        elif message == "kill":
            com = False
            client_socket.send(message.encode())
        else:
            client_socket.send(message.encode())
            data = client_socket.recv(1024).decode()
            if data == "bye":
                com = False
            else:
                print(f"Message reçu= {data}")
    client_socket.close()

echange = threading.Thread(target=echange)