import socket
import psutil
import platform
import subprocess
import os,sys

def restart():
    print("restart now")
    print("...")
    print("restarted")
    os.execv(sys.executable, ['python'] + sys.argv)

def ping(val:str):
    if OS[0] == "Windows":
        result = subprocess.check_output("ping "+val,shell=True).decode("cp850")
        return result
    else:
        command = subprocess.run(["ping", val, "-c", "1", "-W", "2"], capture_output=True)
        result = command.stdout.decode()
        return result

def command_linux(input:str):
    return subprocess.check_output(input, shell=True).decode("cp850").strip()

def command_powershell(input:str):
    return subprocess.check_output(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", input],shell=True).decode("cp850")

def command_dos(input:str):
    if "mkdir" in input:
        path = os.getcwd()
        input=input.split(" ")
        path+=f"\{input[1]}"
        try:
            os.mkdir(path, mode = 0o777)
        except FileExistsError:
            return "dossier deja crée"
        else:
            return "dossier bien crée"
    else:
        return subprocess.check_output(input, shell=True).decode("cp850").strip()

if __name__ == "__main__":
    host="0.0.0.0"
    port= 8040
    com=True
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    OS = platform.uname()

    while com:
        try:
            data = conn.recv(1024).decode()
        except:
            conn, address = server_socket.accept()
        else:
            if data.lower() == "disconnect":
                conn, address = server_socket.accept()
                com = False
            elif data.lower() == "reset":
                restart()
            elif data.lower() == "kill":
                conn.close()
                print("Server éteint")
                com = False
            elif data.lower() == "os":
                conn.send(f"La machine utilise le système d'exploitation: {OS[0]}".encode())
            elif data.lower() == "ram":
                RAM = psutil.virtual_memory()
                conn.send(f"La RAM totale est d'environ: {round(RAM[0]/10**9,1)}Gb, la RAM utilisé est d'environ: {round(RAM[3]/10**9,1)}Gb, la RAM restante est d'environ: {round(RAM[4]/10**9,1)}Gb".encode())
            elif data.lower() == "cpu":
                conn.send(f"Actuellement, le CPU utilise: {psutil.cpu_percent(1)}% de ses capacités.".encode())
            elif data.lower() == "ip":
                conn.send(f"L'adresse IP de la machine est: {socket.gethostbyname(socket.gethostname())}".encode())
            elif data.lower() == "name":
                conn.send(f"Le nom de la machine est: {OS[1]}".encode())
            elif data.lower() == "connexion information":
                conn.send(f"L'adresse IP de la machine est: {socket.gethostbyname(socket.gethostname())} et le nom de la machine est {OS[1]}".encode())

            elif "powershell:" in data.lower():
                if OS[0] == "Windows":
                    data=data.split(":")
                    conn.send(f"Voici le résultat de la commmande get-process: {command_powershell(data[1])}".encode())
                else:
                    conn.send("Le système d'exploitation est incorrect.".encode())
            elif "linux:" in data.lower():
                if OS[0] == "Linux":
                    data=data.split(":")
                    conn.send(f"Voici le résultat de la commmande {data[1]}: {command_linux(data[1])}".encode())
                else:
                    conn.send("Le système d'exploitation est incorrect.".encode())
            elif "dos:" in data.lower():
                if OS[0] == "Windows":
                    data=data.split(":")
                    if "mkdir" in data[1]:
                        command_dos(data[1])
                        conn.send(f"Voici le résultat de la commmande {data[1]}: {command_dos(data[1])}".encode())
                    else:
                        conn.send(f"Voici le résultat de la commmande {data[1]}: {command_dos(str(data[1]))}".encode())
                else:
                    conn.send("Le système d'exploitation est incorrect.".encode())
            elif data.lower() == "python --version":
                command = subprocess.run(["python", "--version"], capture_output=True)
                result=command.stderr.decode('windows-1252')
                conn.send(f"Voici le résultat de la commmande python --version: {result}".encode())
            elif "ping" in data.lower():
                try:
                    data=data.split(" ")
                    result=ping(data[1])
                except:
                    conn.send(f"Ping échoué".encode())
                else:
                    conn.send(result.encode())
            elif data.lower()=="xetyauibeabfa":
                conn.send("Connecté".encode())
            else:
                conn.send("commande inconnue".encode())