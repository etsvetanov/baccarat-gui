__author__ = 'etsvetanov'

from PyQt5.QtWidgets import (QWidget, QPushButton,
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

        self.lbl = QLabel('$0')
        self.lbl.setFrameShape(QFrame.WinPanel)
        self.lbl.setFrameShadow(QFrame.Sunken)
        self.lbl.setMinimumHeight(30)
        self.lbl.setMinimumWidth(100)
        self.lbl.setStyleSheet("""
                        .QLabel {
                            color: red
                        }
                    """)
        lbl2 = QLabel('Bet: ')

        hlabels = ['partner', 'play', 'level', 'index', 'bet', 'result', 'net']
        vlabels = [gambler.name for gambler in self.game.gamblers]

        self.tbl = QTableWidget(len(vlabels), len(hlabels))
        self.tbl.setHorizontalHeaderLabels(hlabels)
        self.tbl.setVerticalHeaderLabels(vlabels)

        lbl_box = QHBoxLayout()
        lbl_box.addWidget(lbl2)
        lbl_box.addWidget(self.lbl)
        lbl_box.addStretch(1)

        btn_box = QHBoxLayout()
        btn_box.addWidget(btn1)
        btn_box.addWidget(btn2)
        btn_box.addLayout(lbl_box)
        btn_box.addStretch(1)

        tbl_box = QHBoxLayout()
        tbl_box.addWidget(self.tbl)

        layout = QVBoxLayout()
        layout.addLayout(btn_box)
        layout.addLayout(tbl_box)
        layout.addStretch(1)
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
        p = self.game.gamblers[-1]
        self.lbl.setText('  $' + str(p.bet_size) + ' on ' + p.bet_choice.upper())

    def populate_table(self):
        data = []
        for g in self.game.gamblers:
            row = self.game.cltr.player_data[g.name][-1]
            data.append(row)

        for i in range(len(data)):
            for j in range(len(data[i])):
                self.tbl.setItem(i, j, QTableWidgetItem(str(data[i][j])))



