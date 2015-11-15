__author__ = 'evgeni'
from core import *
from data_visualization import *
from gui import GUI
from PyQt5.QtWidgets import QApplication
import datetime
import sys


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

    # strat_test_pair()
    # strat_test_base()
