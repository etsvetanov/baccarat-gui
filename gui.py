__author__ = 'etsvetanov'

import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from .core import *
from data_visualization import Collector


class Example(QMainWindow):

    def __init__(self, table):
        super().__init__()

        self.table = table
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


def factory():
    strat1 = PairStrategy()
    strat2 = PairStrategy()
    strat3 = PairStrategy()
    strat4 = PairStrategy()

    collector = Collector()

    p1 = Player(strategy=strat1, name='P1', cltr=collector)
    p2 = Player(strategy=strat2, name='P2', cltr=collector)
    p3 = Player(strategy=strat3, name='P3', cltr=collector)
    p4 = Player(strategy=strat4, name='P4', cltr=collector)

    p1.strategy.set_pair(p2)
    p2.strategy.set_pair(p1)
    p3.strategy.set_pair(p4)
    p4.strategy.set_pair(p3)

    players = [p1, p2, p3, p4]

    strat5 = OverseerStrategy(minions=players)
    p5 = Overseer(strategy=strat5, name='RealPlayer', cltr=collector)

    table = Game(cltr=collector, gamblers=players + [p5], max_rounds=1000)

    return table, collector


if __name__ == '__main__':

    table, collector = factory()

    app = QApplication(sys.argv, table)
    ex = Example()
    sys.exit(app.exec_())
