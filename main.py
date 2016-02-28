__author__ = 'evgeni'

from gui import GUI
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())



# TODO: add unit tests
# TODO: add a progress bar/counter for simulation [x]
# TODO: add excel export function
# TODO: add a light-weight simulation (collect only net?)