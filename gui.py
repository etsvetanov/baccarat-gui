__author__ = 'etsvetanov'

from PyQt5.QtWidgets import (QWidget, QMainWindow, QPushButton, QApplication,\
    QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QFrame)


class GUI(QWidget):

    def __init__(self, game):
        super().__init__()

        self.game = game
        self.lbl = None
        self.tbl = None
        self.initUI()

    def initUI(self):

        btn1 = QPushButton("Player")
        btn2 = QPushButton("Bank")
        for btn in [btn1, btn2]:
            btn.setMinimumWidth(100)
            btn.setMinimumHeight(70)

        self.lbl = QLabel(' This is sometext')
        self.lbl.setFrameShape(QFrame.WinPanel)
        self.lbl.setFrameShadow(QFrame.Sunken)
        # self.lbl.setContentsMargins(15, 15, 15, 15)
        self.lbl.setMinimumHeight(30)
        self.lbl.setMinimumWidth(100)
        hlabels = ['partner', 'play', 'index', 'bet', 'result', 'net']
        vlabels = [gambler.name for gambler in self.game.gamblers]

        self.tbl = QTableWidget(len(vlabels), len(hlabels))
        self.tbl.setHorizontalHeaderLabels(hlabels)
        self.tbl.setVerticalHeaderLabels(vlabels)

        lbl_box = QHBoxLayout()
        lbl_box.addWidget(self.lbl)
        lbl_box.addStretch(1)

        # lbl_box.setContentsMargins(10, 10, 10, 10)

        hbox = QHBoxLayout()
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(lbl_box)
        layout.addLayout(hbox)
        layout.addWidget(self.tbl)
        layout.addStretch(1)
        # tbl.resizeColumnsToContents()
        # tbl.resizeRowsToContents()
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.setLayout(layout)
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('Event Sender')
        self.show()

    def buttonClicked(self):

        sender = self.sender()
        self.game.deal(sender.text().lower())
        self.populate_table()
        self.lbl.setText(sender.text().lower())

    def populate_table(self):
        data = []
        for g in self.game.gamblers:
            row = []
            try:
                row.append(g.strategy.pair.name)
            except AttributeError:
                row.append('-')

            row += g.bet_choice, g.strategy.last_index, g.bet_size, g.res, g.statistics['net']
            data.append(row)

        for i in range(len(data)):
            for j in range(len(data[i])):
                self.tbl.setItem(i, j, QTableWidgetItem(str(data[i][j])))



