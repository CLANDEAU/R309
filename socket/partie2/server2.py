import socket
import threading

if __name__=='__main__':
    host="127.0.0.1"
    port= 10006

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    connexion=True

    def recep():
        global connexion
        global conn
        while connexion:
            data = conn.recv(1024).decode()
            if data == "bye":
                print(f"\nMessage reçu= {data}")
                print("Le client s'est déconnecté")
                connexion=False
            elif data == "arret":
                print("Connexion fermé")
                conn.close()
            else:
                print(f"\nMessage reçu= {data}")
        while connexion is False:
            conn, address = server_socket.accept()
            connexion = True
    def envoi():
        global connexion
        global conn
        while connexion:
            reply = input("Message envoyé= ")
            if reply=="bye":
                connexion = False
                conn.send(reply.encode())
                print("Le client a été déconnecté")
            elif reply == "arret":
                conn.send(reply.encode())
                print("Connexion fermé")
                conn.close()
            else:
                conn.send(reply.encode())
        while connexion is False:
            conn, address = server_socket.accept()
            connexion = True



    envoi = threading.Thread(target=envoi)
    recep = threading.Thread(target=recep)

    envoi.start()
    recep.start()

    recep.join()
    envoi.join()
