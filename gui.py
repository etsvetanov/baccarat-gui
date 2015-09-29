__author__ = 'etsvetanov'

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication


class Example(QMainWindow):

    def __init__(self, game):
        super().__init__()

        self.table = game
        self.initUI()

    def initUI(self):

        btn1 = QPushButton("Player", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Bank", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Event Sender')
        self.show()

    def buttonClicked(self):

        sender = self.sender()
        self.statusBar().showMessage(sender.text() + 'was pressed')
        self.table.deal(sender.text().lower())
