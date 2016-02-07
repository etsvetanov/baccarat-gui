__author__ = 'evgeni'

from gui import GUI
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

