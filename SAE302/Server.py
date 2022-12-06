import socket
import psutil
import platform
import subprocess
import os,sys

def restart():
    print("restart now")
    os.execv(sys.executable, ['python'] + sys.argv)

host="127.0.0.1"
port= 8006
com=True
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)
conn, address = server_socket.accept()

while com:
    data = conn.recv(1024).decode()
    OS = platform.uname()
    if data == "disconnect":
        conn, address = server_socket.accept()
    elif data == "reset":
        restart()
    elif data == "clear":
        conn.send("clear".encode())
    elif data == "OS":
        print(f"{OS[0]}")
        conn.send(f"La machine utilise le système d'exploitation: {OS[0]}".encode())
    elif data == "RAM":
        RAM = psutil.virtual_memory()
        conn.send(f"La RAM totale est d'environ: {round(RAM[0]/10**9,1)}Gb, la RAM utilisé est d'environ: {round(RAM[3]/10**9,1)}Gb, la RAM restante est d'environ: {round(RAM[4]/10**9,1)}Gb".encode())
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
    elif data == "Linux:ls -la":
        if OS[0] == "Linux":
            command = subprocess.run(["ls","-la"], capture_output=True)
            result = command.stdout.decode('windows-1252')
            conn.send(f"Voici le résultat de la commmande ls -la: {result}".encode())
        else:
            conn.send("Le système d'exploitation est incorrect.".encode())
    elif data == "DOS:dir":
        if OS[0] == "Windows":
            command = subprocess.run(["-Command", "dir"], capture_output=True)
            result = command.stdout.decode('windows-1252')
            conn.send(f"Voici le résultat de la commmande dir: {result}".encode())
        else:
            conn.send("Le système d'exploitation est incorrect.".encode())
    elif data == "DOS:mdir toto":
        if OS[0] == "Windows":
            command = subprocess.run(["mdir", "toto"], capture_output=True)
            result = command.stdout.decode('windows-1252')
            conn.send(f"Voici le résultat de la commmande mdir toto: {result}".encode())
        else:
            conn.send("Le système d'exploitation est incorrect.".encode())
    elif data == "python --version":
        command = subprocess.run(["python", "--version"], capture_output=True)
        result=command.stderr.decode('windows-1252')
        conn.send(f"Voici le résultat de la commmande python --version: {result}".encode())
    elif data == "ping 192.157.65.78":
        if OS[0] == "Windows":
            conn.send("ping 192.157.65.78".encode())
        else:
            command = subprocess.run(["ping","192.157.65.78","-c","1","-W","2"],capture_output=True)
            result=command.stdout.decode()
            conn.send(f"Voici le résultat de la commmande ping 192.157.65.78: {result}".encode())

    else:
        print(f"Message reçu= {data}")

