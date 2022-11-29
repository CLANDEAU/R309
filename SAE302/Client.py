import socket
import threading
import subprocess
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWidgets import QApplication

class Socket:
    def __init__(self,host="127.0.0.1",port=8004):
        self.__host=host
        self.__port = port
        self.__client_socket = socket.socket()
        self.__client_socket.connect((host, port))

    def echange(self):
        com = True
        while com:
            message = input("Message envoyé=")
            if message == "disconnect":
                com = False
                self.__client_socket.send(message.encode())
            elif message == "kill":
                com = False
                self.__client_socket.send(message.encode())
            elif message == "reset":
                self.__client_socket.send(message.encode())
            else:
                self.__client_socket.send(message.encode())
                data = self.__client_socket.recv(100000).decode()
                if data == "disconnect":
                    com = False
                elif data == "ping 192.157.65.78":
                    print("Voici le résultat de la commmande ping 192.157.65.78:")
                    subprocess.Popen('ping 192.157.65.78')
                else:
                    print(data)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        grid = QGridLayout()
        widget.setLayout(grid)

        self.__temp = QLabel("Temperature")
        self.__text = QLineEdit("")
        self.__temp2 = QLabel("°C")
        self.__temp3 = QLabel("Conversion")
        self.__temp4 = QLabel("K")
        self.__conv = QPushButton("Convertir")
        self.__interrogation = QPushButton("?")
        self.__answer = QLineEdit("")
        self.__answer.setEnabled(False)
        self.__cb = QComboBox()
        self.__cb.addItem("°C -> K")
        self.__cb.addItem("K -> °C")
        self.__msgBox=QMessageBox()
        self.__msgBox.setText("Permet de convertir un nombre soit de Kelvin vers Celcius, soit de Celcius vers Kelvin")
        self.__msgBox.setWindowTitle("Aide")
        self.__msgBox2 = QMessageBox()
        self.__msgBox2.setText("Erreur, il faut entrer un float.")
        self.__msgBox2.setWindowTitle("Erreur")
        grid.addWidget(self.__temp, 0, 0)
        grid.addWidget(self.__temp2, 0, 2)
        grid.addWidget(self.__text, 0,1)
        grid.addWidget(self.__conv, 1,1)
        grid.addWidget(self.__cb, 1, 2)
        grid.addWidget(self.__answer, 2, 1)
        grid.addWidget(self.__temp3, 2, 0)
        grid.addWidget(self.__temp4, 2, 2)
        grid.addWidget(self.__interrogation, 3, 3)


        self.__conv.clicked.connect(self._actionConv)
        self.__interrogation.clicked.connect(self._actionInterrogation)
        self.__cb.currentTextChanged.connect(self._Combobox_change)

        self.setWindowTitle("Charles")
    def _actionConv(self):
        try:
            temp_recup=float(self.__text.text())
        except:
            self.__msgBox2.exec()
            self.__text.setText("")
        else:
            if self.__cb.currentText() == "°C -> K":
                res=temp_recup+273.15
                self.__answer.setText(f"{res}")
            else:
                res=temp_recup-273.15
                self.__answer.setText(f"{res}")
    def _actionInterrogation(self):
        self.__msgBox.exec()
    def _Combobox_change(self):
        if self.__cb.currentText()=="°C -> K":
            self.__temp2.setText("°C")
            self.__temp4.setText("K")
        else:
            self.__temp4.setText("°C")
            self.__temp2.setText("K")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

socket1=Socket()
echange = threading.Thread(target=socket1.echange)
echange.start()
echange.join()


