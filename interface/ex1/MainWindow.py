from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        grid = QGridLayout()
        widget.setLayout(grid)

        self.__lab = QLabel("Saisir votre nom")
        self.__text = QLineEdit("")
        self.__ok = QPushButton("Ok")
        self.__quit = QPushButton("Quitter")
        self.__answer = QLabel("")

        grid.addWidget(self.__lab, 0, 0)
        grid.addWidget(self.__text, 1,0)
        grid.addWidget(self.__ok, 3,0)
        grid.addWidget(self.__quit, 3, 1)
        grid.addWidget(self.__answer, 2, 0)

        self.__ok.clicked.connect(self._actionOk)
        self.__quit.clicked.connect(self._actionQuitter)

        self.setWindowTitle("Charles")
    def _actionOk(self):
        self.__answer.setText(self.__text.text())
    def _actionQuitter(self):
        QCoreApplication.exit(0)
