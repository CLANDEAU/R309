import socket
import threading
import subprocess
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWidgets import QApplication

class Socket:
    def __init__(self,host="127.0.0.1",port=8005):
        self.__host=host
        self.__port = port
        self.__client_socket = socket.socket()
        message = "Connecté"
        self.__message = message
    def get_msg(self):
        return self.__message
    def set_msg(self,msg):
        self.__message = msg
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
        widget = QWidget()
        self.setCentralWidget(widget)

        grid = QGridLayout()
        widget.setLayout(grid)

        self.setGeometry(0, 0, 1920, 1080)
        self.__print = QLineEdit("print")
        self.setWindowTitle("Charles")
        self.__ter=QLabel("")

        grid.addWidget(self.__print, 0, 0)
        grid.addWidget(self.__ter, 0, 1)
        self.__conv = QPushButton("Se connecter")
        self.__conv.clicked.connect(self.connection)
        self.__send = QPushButton("Envoyer")
        grid.addWidget(self.__conv, 1, 0)
        self.__send.clicked.connect(self.send)
        grid.addWidget(self.__send, 1, 1)
    def connection(self):
        self.__soc=Socket()
        self.__soc.connect()
    def send(self):
        msg=Socket.set_msg(self.__soc,self.__print.text())
        self.__ter.setText(Socket.echange(self.__soc, msg))
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()





"""

socket1=Socket()
echange = threading.Thread(target=socket1.echange)
echange.start()
echange.join()

args=[Socket.get_msg]
"""