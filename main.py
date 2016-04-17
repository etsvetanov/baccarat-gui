__author__ = 'evgeni'

from gui import GUI
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

    # TODO: add a class BigButton that sets the size and stuff in the __init__
    # TODO: add a reset button (begin a new game)
    # TODO: add a setting window to add/remove columns and more stuff
    # TODO: add a light-weight simulation (collect only net?)
    # TODO: add a setting to drop the game at certain point and begin a new one
    # TODO: make list of statistic items (partner, self.bet_choice, level, index, bet, self.res, target, self.statistics['net']) that is taken from one place only,
    # so that it is changed from one place only
    # TODO: add unit tests
    # TODO: use qt designer


