import socket

if __name__=='__main__':
    host="127.0.0.1"
    port= 10000
    com=True

    client_socket = socket.socket()
    client_socket.connect((host, port))

    while com:
        message=input("Message envoyé= ")
        client_socket.send(message.encode())
        data =client_socket.recv(1024).decode()
        print(f"Message reçu= {data}")
    client_socket.close()