import socket
import threading
import time

host="127.0.0.1"
port= 10006

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)
conn, address = server_socket.accept()
connexion=True

def recep(conn):
    global connexion
    while connexion:
        data = conn.recv(1024).decode()
        if data == "arret":
            print("Connexion close")
            print("finito")
            conn.close()
        elif data == "bye":
            print(f"\nMessage reçu= {data}")
            print("deco")
            connexion=False
        else:
            print(f"\nMessage reçu= {data}")
    while connexion is False:
        conn, address = server_socket.accept()


def envoi(conn):
    global connexion
    while connexion:
        reply = input("Message envoyé= ")
        if reply=="bye":
            conn.send(reply.encode())
            print("deco")
            connexion=False
        elif reply == "arret":
            conn.send(reply.encode())
            print("finito")
            conn.close()
        else:
            conn.send(reply.encode())
    while connexion is False:
        conn, address = server_socket.accept()


envoi = threading.Thread(target=envoi,args=[conn])
recep = threading.Thread(target=recep,args=[conn])

envoi.start()
recep.start()

recep.join()
envoi.join()