import socket

if __name__=='__main__':
    host="127.0.0.1"
    port= 65002
    com=True
    try:
        server_socket = socket.socket()
        server_socket.bind((host, port))
        server_socket.listen(1)
        conn, address = server_socket.accept()
        while com:
            data = conn.recv(1024).decode()
            if data == "arret":
                com=False
                conn.close()
            elif data == "bye":
                print(f"Message reçu= {data}")
                conn, address = server_socket.accept()
            else:
                print(f"Message reçu= {data}")
                reply=input("Message envoyé= ")
                if reply == "bye":
                    conn.send(reply.encode())
                    conn, address = server_socket.accept()
                elif reply == "arret":
                    print("Arret du serv")
                    com = False
                    conn.close()
                else:
                    conn.send(reply.encode())
    except:
        print("Une erreur a été rencontré")
