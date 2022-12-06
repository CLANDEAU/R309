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
        message = "Connecté"
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
        self.__client_socket.connect((self.__host, self.__port))
    def send(self,message):
        self.__client_socket.send(message.encode())
        data = self.__client_socket.recv(100000).decode()
        if data == "disconnect":
            self.__com= False
        elif data == "ping 192.157.65.78":
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

        self.__print = QLineEdit("OS") #Powershell:get-process
        self.__ter = QTextEdit()
        self.__conn = QPushButton("Se connecter au server")
        self.__send = QPushButton("Envoyez le message au server")
        self.__send.setEnabled(False)
        self.__ip2 = QLabel("Entrez l'adresse IP de la machine:")
        self.__ip1 = QLineEdit("127.0.0.1")
        self.__port2 = QLabel("Entrez le port de la machine:")
        self.__port1 = QLineEdit("8006")
        self.__add = QPushButton("Ajouter un server")
        self.__msgBox = QMessageBox()
        self.__msgBox.setText("Permet de convertir un nombre soit de Kelvin vers Celcius, soit de Celcius vers Kelvin")
        self.__msgBox.setWindowTitle("Aide")

        grid.addWidget(self.__print, 0,0 , 1,6)
        grid.addWidget(self.__ter, 1,0 , 1,6)
        grid.addWidget(self.__ip1, 2,1 , 1,1)
        grid.addWidget(self.__ip2, 2,0 , 1,1)
        grid.addWidget(self.__port1, 2,4 , 1,1)
        grid.addWidget(self.__port2, 2,3 , 1, 1)
        grid.addWidget(self.__conn, 3,0 , 1,3)
        grid.addWidget(self.__send, 3,3 , 1,3)
        grid.addWidget(self.__add, 4, 0, 1,6)

        self.__send.clicked.connect(self.send)
        self.__conn.clicked.connect(self.connection)
    def connection(self):
        port = int(self.__port1.text())
        host = str(self.__ip1.text())
        self.__soc = Socket(host,port)
        self.__soc.connect()
        self.__send.setEnabled(True)
    def send(self):
        Socket.set_msg(self.__soc, self.__print.text())
        msg = Socket.get_msg(self.__soc)
        thread = threading.Thread(target=Socket.send, args=[self.__soc,msg])
        thread.start()
        self.__ter.append(Socket.send(self.__soc,msg))
        thread.join()
        if msg == "clear":
            self.__ter.clear()
    def set_title(self,title):
        self.setWindowTitle(title)

list=[]
nb=int(input("A comien de server voulez-vous vous connecter: "))
for i in range(nb):
    name = str(input(f"Veuillez nommer votre server n°{i+1}: "))
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