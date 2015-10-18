__author__ = 'evgeni'
from core import *
from data_visualization import *
from gui import GUI
from PyQt5.QtWidgets import QApplication
import datetime
import sys


def strat_test_base():
    start = datetime.datetime.now().time()
    strat1 = BaseStrategy()
    strat2 = BaseStrategy()
    strat3 = BaseStrategy()
    collector = Collector()
    p1 = Player(strategy=strat1, name='P1', cltr=collector)
    p2 = Player(strategy=strat2, name='P2', cltr=collector)
    p3 = Player(strategy=strat3, name='P3', cltr=collector)
    table = Game(collector)
    players = [p1, p2, p3]

    for num in range(10000):
        table.register(players)
    table.plotz()

    ss = SpreadSheet(collector)
    ss.create_spreadsheet()

    print('times')
    print('start:', start)
    print('end:', datetime.datetime.now().time())


def strat_test_pair():
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
    table.run(1000)

    print('Plotting the results...')
    table.plotz()
    print('Filling in the spreadsheet data...')
    ss = SpreadSheet(collector)
    ss.create_spreadsheet()


def factory():
    strat1 = PairStrategy()
    strat2 = PairStrategy()
    strat3 = PairStrategy()
    strat4 = PairStrategy()

    collector = Collector()

    p2 = Player(strategy=strat2, name='P2', cltr=collector)
    p1 = Player(strategy=strat1, name='P1', cltr=collector)
    p3 = Player(strategy=strat3, name='P3', cltr=collector)
    p4 = Player(strategy=strat4, name='P4', cltr=collector)

    p1.strategy.set_pair(p2)
    p2.strategy.set_pair(p1)
    p3.strategy.set_pair(p4)
    p4.strategy.set_pair(p3)

    players = [p1, p2, p3, p4]

    strat5 = OverseerStrategy(minions=players)
    p5 = Overseer(strategy=strat5, name='RealPlayer', cltr=collector)

    tbl = Game(cltr=collector, gamblers=players + [p5], max_rounds=1000)

    return collector, tbl


if __name__ == '__main__':
    cltr, game = factory()

    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

    # strat_test_pair()
    # strat_test_base()
