import socket

if __name__=='__main__':
    host="127.0.0.1"
    port= 10000
    com=True

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    conn2, address2 = server_socket.accept()
    list=["pierre","ciseau","feuille"]

    while com:
        data = conn.recv(1024).decode()
        data2 = conn2.recv(1024).decode()
        if data in list and data2 in list:
            if data == "pierre" and data2 == "ciseau":
                conn.send("Bien joué".encode())
                conn2.send("Perdu".encode())
            elif data == "ciseau" and data2=="feuille":
                conn.send("Bien joué".encode())
                conn2.send("Perdu".encode())
            elif data == "feuille" and data2 == "pierre":
                conn.send("Bien joué".encode())
                conn2.send("Perdu".encode())
            elif data2 == "pierre" and data == "ciseau":
                conn2.send("Bien joué".encode())
                conn.send("Perdu".encode())
            elif data2 == "ciseau" and data=="feuille":
                conn2.send("Bien joué".encode())
                conn.send("Perdu".encode())
            elif data2 == "feuille" and data == "pierre":
                conn2.send("Bien joué!".encode())
                conn.send("Perdu!".encode())
            elif data == "pierre" and data2 == "pierre":
                conn.send("match nul :(".encode())
                conn2.send("match nul :(".encode())
            elif data == "ciseau" and data2=="ciseau":
                conn.send("match nul :(".encode())
                conn2.send("match nul :(".encode())
            elif data == "feuille" and data2 == "feuille":
                conn.send("match nul :(".encode())
                conn2.send("match nul :(".encode())
        else:
            conn.send("Veuillez choisir entre: pierre, ciseau, feuille".encode())
            conn2.send("Veuillez choisir entre: pierre, ciseau, feuille".encode())



