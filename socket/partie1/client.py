import socket

if __name__=='__main__':
    host="127.0.0.1"
    port= 65002
    com=True
    try:
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
                data = client_socket.recv(1024).decode()
                if data == "bye":
                    com=False
                else:
                    print(f"Message reçu= {data}")
        client_socket.close()
    except:
        print(f"\nVous vous êtes déconnectez d'une manière peu recommandé.")