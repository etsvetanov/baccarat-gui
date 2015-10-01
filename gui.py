__author__ = 'etsvetanov'

from PyQt5.QtWidgets import (QWidget, QMainWindow, QPushButton, QApplication,\
    QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout)


class GUI(QWidget):

    def __init__(self, game):
        super().__init__()

        self.game = game
        self.initUI()
        self.lbl = None

    def initUI(self):

        btn1 = QPushButton("Player")
        btn2 = QPushButton("Bank")
        self.lbl = QLabel('This is sometext')
        hlabels = ['play', 'index', 'bet', 'result', 'net', 'partner']
        vlabels = [gambler.name for gambler in self.game.gamblers]

        tbl = QTableWidget(len(vlabels), len(hlabels))
        tbl.setHorizontalHeaderLabels(hlabels)
        tbl.setVerticalHeaderLabels(vlabels)

        hbox = QHBoxLayout()
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addStretch(1)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl)
        layout.addLayout(hbox)
        layout.addWidget(tbl)
        # tbl.resizeColumnsToContents()
        # tbl.resizeRowsToContents()
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.setLayout(layout)
        self.setGeometry(300, 300, 700, 300)
        self.setWindowTitle('Event Sender')
        self.show()

    def buttonClicked(self):

        sender = self.sender()
        self.game.deal(sender.text().lower())
        self.lbl.setText(sender.text().lower())
