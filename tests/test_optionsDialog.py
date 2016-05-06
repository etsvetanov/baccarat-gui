from unittest import TestCase
from PyQt5.QtWidgets import QApplication, QHBoxLayout
from gui import OptionsDialog


class TestOptionsDialog(TestCase):
    def test_initUI(self):
        pass

    def test_create_box_strategy(self):
        app = QApplication([])

        class Mockup:
            options_dic = None
            mplier = 1
            p_num = 1
            starting_bet = 1

        main = Mockup()
        options = OptionsDialog(main)
        box = options.create_box_strategy()

        self.assertEqual(type(box), type(QHBoxLayout))
