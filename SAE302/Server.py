import socket

host="127.0.0.1"
port= 8000
com=True
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)
conn, address = server_socket.accept()

while com:
    data = conn.recv(1024).decode()
    if data == "disconnect":
        print(f"Message reçu= {data}")
        conn, address = server_socket.accept()
    elif data == "kill":
        conn.close()
    else:
        print(f"Message reçu= {data}")