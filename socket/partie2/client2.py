import socket
import threading

if __name__=='__main__':
    host="127.0.0.1"
    port= 10006
    client_socket = socket.socket()
    client_socket.connect((host, port))

    def envoi(client_socket):
        while True:
            message = input("Message envoyé= ")
            if message == "arret":
                client_socket.send(message.encode())
                client_socket.close()
            elif message == "bye":
                client_socket.send(message.encode())
                client_socket.close()
            else:
                client_socket.send(message.encode())

    def recep(client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            if data=="bye":
                print(f"\nMessage reçu= {data}")
                client_socket.close()
            else:
                print(f"\nMessage reçu= {data}")

    envoi = threading.Thread(target=envoi,args=[client_socket])
    recep = threading.Thread(target=recep,args=[client_socket])

    envoi.start()
    recep.start()



