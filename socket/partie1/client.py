import socket

host="127.0.0.1"
port= 65002
com=True

client_socket = socket.socket()
client_socket.connect((host, port))

while com:
    message=input("Message envoyé= ")
    if message=="arret":
        com=False
        client_socket.send(message.encode())
    elif message=="bye":
        com = False
        client_socket.send(message.encode())
    else:
        client_socket.send(message.encode())
        data =client_socket.recv(1024).decode()
        print(f"Message reçu= {data}")
client_socket.close()
