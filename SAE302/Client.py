import socket
import threading
import subprocess
from PyQt5 import QtCore , QtGui,QtWidgets
from PyQt5.QtWidgets import *
import sys

class Socket:
    def __init__(self,host,port):
        self.__host = host
        self.__port = port
        self.__client_socket = socket.socket()
        message ="xetyauibeabfa"
        self.__message = message

    def get_msg(self):
        return self.__message
    def set_msg(self,msg):
        self.__message = msg
    def set_host(self,host):
        self.__host = host
    def set_port(self,port):
        self.__port = port
    def connect(self):
        try:
            self.__client_socket.connect((self.__host, self.__port))
        except:
            self.__message="erreur de connexion"
        else:
            return True
    def send(self,message):
        try:
            self.__client_socket.send(message.encode())
            data = self.__client_socket.recv(100000).decode()
        except:
            self.__message="Erreur de connexion"
        else:
            if data == "ping 192.157.65.78":
                print("Voici le résultat de la commmande ping 192.157.65.78:")
                print(subprocess.Popen('ping 192.157.65.78'))
            else:
                return data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        title=""
        self.__title = title
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle(self.__title)
        self.setGeometry(0, 0, 400,400)
        count=0
        self.__count=count

        self.__print = QLineEdit("OS") #Powershell:get-process
        self.__ter = QTextEdit()
        self.__conn = QPushButton("Se connecter au server")
        self.__send = QPushButton("Envoyez le message au server")
        self.__send.setEnabled(False)
        self.__ip2 = QLabel("Entrez l'adresse IP de la machine:")
        self.__ip1 = QLineEdit("")
        self.__port2 = QLabel("Entrez le port de la machine:")
        self.__port1 = QLineEdit("")
        self.__act = QPushButton("Actualiser")

        grid.addWidget(self.__print, 0,0 , 1,6)
        grid.addWidget(self.__ter, 1,0 , 1,6)
        grid.addWidget(self.__ip1, 2,1 , 1,1)
        grid.addWidget(self.__ip2, 2,0 , 1,1)
        grid.addWidget(self.__port1, 2,4 , 1,1)
        grid.addWidget(self.__port2, 2,3 , 1,1)
        grid.addWidget(self.__conn, 3,0 , 1,3)
        grid.addWidget(self.__send, 3,3 , 1,3)
        grid.addWidget(self.__act, 4,0, 1,6)

        self.__send.clicked.connect(self.send)
        self.__conn.clicked.connect(self.connection)
        self.__act.clicked.connect(self.actualiser)


    def connection(self):
        port = int(self.__port1.text())
        host = str(self.__ip1.text())
        self.__soc = Socket(host,port)
        self.__soc.connect()
        self.__send.setEnabled(True)
        msg = Socket.get_msg(self.__soc)
        self.__ter.append(Socket.send(self.__soc, msg))
    def send(self):
        Socket.set_msg(self.__soc, self.__print.text())
        msg = Socket.get_msg(self.__soc)
        thread = threading.Thread(target=Socket.send, args=[self.__soc,msg])
        thread.start()
        self.__ter.append(Socket.send(self.__soc,msg))
        thread.join()
        if msg == "clear" or msg== "cls":
            self.__ter.clear()
    def set_title(self,title):
        self.setWindowTitle(title)
    def actualiser(self):
        fichier = open("zoo.txt", "r")
        lignes = fichier.readlines()
        list = []
        ip = []
        port = []
        name1 = []
        for i in range(len(lignes)):
            name = f"Server n°{i + 1}"
            list.append(name)
        for val in range(len(list)):
            list[val] = lignes[val].split(",")
            ip_port = list[val][0]
            ip_port1 = ip_port.split(":")
            ip.append(ip_port1[0])
            port.append(ip_port1[1])
            name1.append(list[val][1])
        self.__ip1.setText(ip[self.__count])
        self.__port1.setText(port[self.__count])
        self.setWindowTitle(name1[self.__count])
        self.__count+=1

        fichier.close()

if __name__ == '__main__':
    fichier = open("zoo.txt", "r")
    lignes = fichier.readlines()
    list = []
    for i in range(len(lignes)):
        name = f"Server n°{i + 1}"
        list.append(name)
    c=-500
    app = QApplication(sys.argv)
    for i in range(len(list)):
        c += 600
        list[i] = MainWindow()
        list[i].setGeometry(c,100,400,400)
        list[i].set_title(f"Server n°{i+1}")
        list[i].show()
    app.exec()
