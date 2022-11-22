import socket
import psutil
import platform
import subprocess

host="127.0.0.1"
port= 8000
com=True
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)
conn, address = server_socket.accept()

while com:
    data = conn.recv(1024).decode()
    OS = platform.uname()
    if data == "disconnect":
        print(f"Message reçu= {data}")
        conn, address = server_socket.accept()
    elif data == "OS":
        conn.send(f"La machine utilise le système d'exploitation: {OS[0]}".encode())
    elif data == "RAM":
        RAM = psutil.virtual_memory()
        conn.send(f"La RAM totale est d'environ: {round(RAM[0]/10**9,1)}, la RAM utilisé est d'environ: {round(RAM[3]/10**9,1)}, la RAM restante est d'environ: {round(RAM[4]/10**9,1)}".encode())
    elif data == "CPU":
        conn.send(f"Actuellement, le CPU utilise: {psutil.cpu_percent(1)}% de ses capacités.".encode())
    elif data == "IP":
        conn.send(f"L'adresse IP de la machine est: {socket.gethostbyname(socket.gethostname())}".encode())
    elif data == "Name":
        conn.send(f"Le nom de la machine est: {OS[1]}".encode())
    elif data == "Connexion information":
        conn.send(f"L'adresse IP de la machine est: {socket.gethostbyname(socket.gethostname())} et le nom de la machine est {OS[1]}".encode())

    elif data == "Powershell:get-process":
        if OS[0] == "Windows":
            command = subprocess.run(["powershell", "-Command", "Get-Process"], capture_output=True)
            result=command.stdout.decode('windows-1252')
            print(result)
            conn.send(f"Voici le résultat de la commmande get-process: {result}".encode())
        else:
            conn.send("Le système d'exploitation est incorrect.".encode())
    elif data == "ls -la":
        if OS[0] == "Linux":
            print("pas encore fait")
        else:
            conn.send("Le système d'exploitation est incorrect.".encode())
    elif data == "DOS:dir":
        if OS[0] == "Mac-OS":
            print("pas encore fait")
        else:
            conn.send("Le système d'exploitation est incorrect.".encode())
    elif data == "DOS:mkdir toto":
        if OS[0] == "Mac-OS":
            print("pas encore fait")
        else:
            conn.send("Le système d'exploitation est incorrect.".encode())
    elif data == "Powershell:get-process":
        if OS[0] == "Mac-OS":
            print("pas encore fait")
        else:
            conn.send("Le système d'exploitation est incorrect.".encode())

    else:
        print(f"Message reçu= {data}")

