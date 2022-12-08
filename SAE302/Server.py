import socket
import psutil
import platform
import subprocess
import os,sys

def restart():
    print("restart now")
    print("...")
    os.execv(sys.executable, ['python'] + sys.argv)

host="127.0.0.1"
port= 8040
com=True
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)
conn, address = server_socket.accept()
OS = platform.uname()

def ping(val:str):
    if OS[0] == "Windows":
        result = subprocess.check_output("ping "+val,shell=True).decode("cp850")
        return result
    else:
        command = subprocess.run(["ping", val, "-c", "1", "-W", "2"], capture_output=True)
        result = command.stdout.decode()
        return result

while com:
    try:
        data = conn.recv(1024).decode()
    except OSError:
        print("Server éteint")
        com=False
    else:
        if data == "Disconnect":
            conn, address = server_socket.accept()
        elif data == "Reset":
            restart()
        elif data == "Kill":
            conn.close()
        elif data == "clear":
            conn.send("clear".encode())
        elif data == "OS":
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
                command = subprocess.run(["dir"], shell=True)
                result = command.stdout.decode('windows-1252')
                conn.send(f"Voici le résultat de la commmande dir: {result}".encode())
            else:
                conn.send("Le système d'exploitation est incorrect.".encode())
        elif data == "DOS:mdir toto":
            if OS[0] == "Windows":
                command = subprocess.run(["mdir", "toto"], shell=True)
                result = command.stdout.decode('windows-1252')
                conn.send(f"Voici le résultat de la commmande mdir toto: {result}".encode())
            else:
                conn.send("Le système d'exploitation est incorrect.".encode())
        elif data == "python --version":
            command = subprocess.run(["python", "--version"], capture_output=True)
            result=command.stderr.decode('windows-1252')
            conn.send(f"Voici le résultat de la commmande python --version: {result}".encode())
        elif "ping" in data:
            try:
                data=data.split(" ")
                result=ping(data[1])
            except:
                conn.send(f"Ping échoué".encode())
            else:
                conn.send(result.encode())
        elif data=="xetyauibeabfa":
            conn.send("connecté".encode())
        else:
            conn.send("commande inconnu".encode())


