__author__ = 'evgeni'

from gui import GUI
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())



    # TODO: make list of statistic items (partner, self.bet_choice, level, index, bet, self.res, target, self.statistics['net']) that is taken from one place only,
    # so that it is changed from one place only
    # TODO: add unit tests
    # TODO: add a progress bar/counter for simulation [x]
    # TODO: add excel export function
    # TODO: add a light-weight simulation (collect only net?)
