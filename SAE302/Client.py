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
            if message == "Disconnect":
                    self.__client_socket.close()
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

        self.__print = QLineEdit("OS")
        self.__ter = QTextEdit()
        self.__conn = QPushButton("Se connecter au server")
        self.__send = QPushButton("OK")
        self.__send1 = QPushButton("OK")
        self.__send.setEnabled(False)
        self.__send1.setEnabled(False)
        self.__ip2 = QLabel("IP de la machine:")
        self.__ip1 = QComboBox()
        self.__port2 = QLabel("Port de la machine:")
        self.__port1 = QLineEdit("")
        self.__port1.setEnabled(False)
        self.__command = QComboBox()
        self.__command.addItem("OS")
        self.__command.addItem("Name")
        self.__command.addItem("IP")
        self.__command.addItem("CPU")
        self.__command.addItem("RAM")
        self.__command.addItem("Connexion information")
        self.__command.addItem("Disconnect")
        self.__command.addItem("Kill")
        self.__command.addItem("Reset")
        self.__ip3 = QLabel("IP nouvelle machine:")
        self.__port3 = QLabel("Port nouvelle machine:")
        self.__add_ip=QLineEdit("")
        self.__add_port = QLineEdit("")
        self.__add = QPushButton("Ajouter le server dans le fichier")

        grid.addWidget(self.__command, 0, 0, 1, 5)
        grid.addWidget(self.__print, 1,0 , 1,5)
        grid.addWidget(self.__ter, 2,0 , 1,6)
        grid.addWidget(self.__ip1, 3,1 , 1,2)
        grid.addWidget(self.__ip2, 3,0 , 1,1)
        grid.addWidget(self.__port1, 3,4 , 1,2)
        grid.addWidget(self.__port2, 3,3 , 1,1)
        grid.addWidget(self.__conn, 4,0 , 1,6)
        grid.addWidget(self.__send, 1,5)
        grid.addWidget(self.__send1, 0,5)
        grid.addWidget(self.__ip3, 5,0)
        grid.addWidget(self.__port3, 5,3)
        grid.addWidget(self.__add_ip, 5,1 , 1,2)
        grid.addWidget(self.__add_port, 5,4 , 1,2)
        grid.addWidget(self.__add,6,0 , 1,6)

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
            if "," in lignes[val]:
                list[val] = lignes[val].split(",")
                ip_port = list[val][0]
                ip_port1 = ip_port.split(":")
                ip.append(ip_port1[0])
                port.append(ip_port1[1])
                name1.append(list[val][1])
                self.__ip1.addItem(ip[val])
                self.__port1.setText(port[0])
            else:
                list[val] = lignes[val].split(":")
                ip.append(list[val][0])
                port.append(list[val][1])
                self.__ip1.addItem(ip[val])
                self.__port1.setText(port[0])
        fichier.close()

        self.__send.clicked.connect(self.send)
        self.__send1.clicked.connect(self.send1)
        self.__conn.clicked.connect(self.connection)
        self.__add.clicked.connect(self.ajouter_serv)
        self.__ip1.currentTextChanged.connect(self._Combobox_change)

    def connection(self):
        port = int(self.__port1.text())
        host = str(self.__ip1.currentText())
        self.__soc = Socket(host,port)
        self.__soc.connect()
        self.__send.setEnabled(True)
        self.__send1.setEnabled(True)
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
    def send1(self):
        Socket.set_msg(self.__soc, self.__command.currentText())
        msg = Socket.get_msg(self.__soc)
        thread = threading.Thread(target=Socket.send, args=[self.__soc,msg])
        thread.start()
        self.__ter.append(Socket.send(self.__soc,msg))
        thread.join()
        if msg == "clear" or msg== "cls":
            self.__ter.clear()
    def set_title(self,title):
        self.setWindowTitle(title)
    def _Combobox_change(self):
        list = []
        ip = []
        port = []
        name1 = []
        for i in range(len(lignes)):
            name = f"Server n°{i + 1}"
            list.append(name)
        for val in range(len(list)):
            if "," in lignes[val]:
                list[val] = lignes[val].split(",")
                ip_port = list[val][0]
                ip_port1 = ip_port.split(":")
                ip.append(ip_port1[0])
                port.append(ip_port1[1])
                name1.append(list[val][1])
                if self.__ip1.currentText()==ip[val]:
                    self.__port1.setText(port[val])
                    self.setWindowTitle(name1[val])
            else:
                list[val] = lignes[val].split(":")
                ip.append(list[val][0])
                port.append(list[val][1])
                if self.__ip1.currentText()==ip[val]:
                    self.__port1.setText(port[val])
    def ajouter_serv(self):
        ip=self.__add_ip.text()
        port=self.__add_port.text()
        fichier = open("zoo.txt", "a")
        fichier.write(f"\n{ip}:{port}")
        fichier.close()

if __name__ == '__main__':
    fichier = open("zoo.txt", "r")
    lignes = fichier.readlines()
    list = []
    for i in range(len(lignes)):
        name = f"Server n°{i + 1}"
        list.append(name)
    x=-500
    y=100
    count2=0
    app = QApplication(sys.argv)
    for i in range(len(list)):
        count2+=1
        x += 600
        if count2>3:
            x = -2300
            for i in range(count2):
                x+=600
                y=600
        if count2>6:
            x = 100
            for i in range(count2):
                y=100
        list[i] = MainWindow()
        list[i].setGeometry(x,y,400,400)
        list[i].set_title(f"Server n°{i+1}")
        list[i].show()
    app.exec()
