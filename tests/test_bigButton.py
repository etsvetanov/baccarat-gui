from unittest import TestCase
from gui import BigButton
from PyQt5.QtWidgets import QApplication


class TestBigButton(TestCase):

    def test_button_size(self):
        app = QApplication([])
        btn = BigButton('test')

        self.assertEqual(btn.minimumWidth(), 100)
