import socket
import threading
import subprocess
from PyQt5.QtCore import QCoreApplication
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
    def echange(self,message):
        com = True
        #message = input("Message envoyé=")
        if self.__message == "disconnect":
            com = False
            self.__client_socket.send(self.__message.encode())
        elif self.__message == "kill":
            com = False
            self.__client_socket.send(self.__message.encode())
        elif self.__message == "reset":
            self.__client_socket.send(self.__message.encode())
        else:
            self.__client_socket.send(self.__message.encode())
            data = self.__client_socket.recv(100000).decode()
            if data == "disconnect":
                com = False
            elif data == "ping 192.157.65.78":
                print("Voici le résultat de la commmande ping 192.157.65.78:")
                print(subprocess.Popen('ping 192.157.65.78'))
            else:
                return data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.i = 0
        widget = QWidget()
        self.setCentralWidget(widget)

        grid = QGridLayout()
        widget.setLayout(grid)
        self.setWindowTitle("Gestionnaire de server")
        self.setGeometry(0, 0, 1500, 900)

        self.__print = QLineEdit("Powershell:get-process")
        self.__ter = QTextEdit()
        self.__conn = QPushButton("Se connecter au server")
        self.__send = QPushButton("Envoyez le message au server")
        self.__send.setEnabled(False)
        self.__ip2 = QLabel("Entrez l'adresse IP de la machine:")
        self.__ip1 = QLineEdit("127.0.0.1")
        self.__port2 = QLabel("Entrez le port de la machine:")
        self.__port1 = QLineEdit("8006")

        grid.addWidget(self.__print, 0,0 , 1,6)
        grid.addWidget(self.__ter, 1,0 , 1,6)
        grid.addWidget(self.__ip1, 2,1 , 1,1)
        grid.addWidget(self.__ip2, 2,0 , 1,1)
        grid.addWidget(self.__port1, 2,4 , 1,1)
        grid.addWidget(self.__port2, 2,3 , 1, 1)
        grid.addWidget(self.__conn, 3,0 , 1,3)
        grid.addWidget(self.__send, 3,3 , 1,3)

        self.__send.clicked.connect(self.send)
        self.__conn.clicked.connect(self.connection)
    def connection(self):
        port = int(self.__port1.text())
        host = str(self.__ip1.text())
        self.__soc = Socket(host,port)
        self.__soc.connect()
        self.__send.setEnabled(True)
    def send(self):
        msg=Socket.set_msg(self.__soc,self.__print.text())
        #self.__ter.setText(Socket.echange(self.__soc, msg))
        self.__ter.append(Socket.echange(self.__soc,msg))
        self.i += 1

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()