__author__ = 'etsvetanov'
from math import floor
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QLabel, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QHBoxLayout, QFrame, QDoubleSpinBox,
                             QSpinBox, QGridLayout)

from factory import GameFactory


class GUI(QWidget):
    def __init__(self):  # TODO: game should not be a parameter
        super().__init__()

        self.game = None  # TODO: self.game should be 'None' and set later when 'BEGIN' is pressed
        self.lbl = None
        self.tbl = None
        self.btn1 = None
        self.btn2 = None
        self.play_layout = None
        self.set_layout = None
        self.layout = None
        self.starting_bet = None
        self.p_num = None
        self.mplier = None
        self.begin_btn = None
        self.preview_box = None

        self.initUI()

    def initUI(self):

        start_lbl = QLabel('Starting bet')
        self.starting_bet = QDoubleSpinBox()
        self.starting_bet.setRange(0.1, 100)
        self.starting_bet.setSingleStep(0.1)
        self.starting_bet.setMinimumHeight(50)
        self.starting_bet.setMinimumWidth(120)
        self.starting_bet.valueChanged.connect(self.update_preview)
        # ----------------------------------
        p_num_lbl = QLabel('Number of pairs')
        self.p_num = QSpinBox()
        self.p_num.setRange(1, 5)
        self.p_num.setMinimumHeight(50)
        self.p_num.setMinimumWidth(120)
        # -----------------------------------
        mplier_lbl = QLabel('Step')
        self.mplier = QSpinBox()
        self.mplier.setRange(2, 5)
        self.mplier.setMinimumHeight(50)
        self.mplier.setMinimumWidth(120)
        self.mplier.valueChanged.connect(self.update_preview)
        self.mplier.setToolTip('The starting bet is multiplied by this value for each consecutive level')
        # -----------------------------------
        self.begin_btn = QPushButton('Begin')
        self.begin_btn.clicked.connect(self.begin)
        self.begin_btn.setMinimumWidth(100)
        self.begin_btn.setMinimumHeight(50)
        begin_lbl = QLabel('')

        self.btn1 = QPushButton("Player")
        self.btn2 = QPushButton("Bank")
        self.btn1.setDisabled(True)
        self.btn2.setDisabled(True)
        self.btn1.clicked.connect(self.buttonClicked)
        self.btn2.clicked.connect(self.buttonClicked)

        for btn in [self.btn1, self.btn2, self]:
            btn.setMinimumWidth(100)
            btn.setMinimumHeight(70)

        self.lbl = QLabel('  $0')
        self.lbl.setFrameShape(QFrame.WinPanel)
        self.lbl.setFrameShadow(QFrame.Sunken)
        self.lbl.setMinimumHeight(30)
        self.lbl.setMinimumWidth(160)
        self.lbl.setStyleSheet("""
                        .QLabel {
                            color: red;
                            font-size: 20px
                        }
                    """)
        lbl2 = QLabel('Bet: ')

        # hlabels = ['partner', 'play', 'level', 'index', 'bet', 'result', 'net']
        # vlabels = [gambler.name for gambler in self.game.gamblers]
        #
        # self.tbl = QTableWidget(len(vlabels), len(hlabels))
        # self.tbl.setHorizontalHeaderLabels(hlabels)
        # self.tbl.setVerticalHeaderLabels(vlabels)

        """----- Layouts ------"""
        """ there is one main layout - VBox - layout """
        """ and two sub-main layouts - set_layout and play_layout """
        """ everything else is a sub layout to either of set_layout or play_layout """
        # set_box = QGridLayout()
        # set_box.addWidget(start_lbl, 0, 0)
        # set_box.addWidget(self.starting_bet, 1, 0)
        # set_box.addWidget(p_num_lbl, 0, 1)
        # set_box.addWidget(p_num, 1, 1)
        # set_box.setColumnMinimumWidth(0, 50)
        # set_box.setColumnMinimumWidth(1, 50)
        # set_box.setColumnStretch(0, 0)
        # set_box.setColumnStretch(1, 0)
        start_box = QVBoxLayout()
        start_box.addWidget(start_lbl)
        start_box.addWidget(self.starting_bet)

        player_box = QVBoxLayout()
        player_box.addWidget(p_num_lbl)
        player_box.addWidget(self.p_num)

        mplier_box = QVBoxLayout()
        mplier_box.addWidget(mplier_lbl)
        mplier_box.addWidget(self.mplier)

        begin_box = QVBoxLayout()
        begin_box.addWidget(begin_lbl)
        begin_box.addWidget(self.begin_btn)
        # a = begin_box.count()
        # b = begin_box.itemAt(0).widget()

        self.preview_box = QGridLayout()

        for i in range(4):
            for j in range(10):
                # label = QLabel(str(i) + ',' + str(j))
                label = QLabel('[' + str(j) + ']')
                self.preview_box.addWidget(label, i, j)

        level_labels_box = QGridLayout()
        level_labels_box.addWidget(QLabel(''), 0, 0)
        for i in range(1, 4):
            label = QLabel('Level' + str(i))
            level_labels_box.addWidget(label, i, 0)

        self.update_preview()
        self.set_layout = QHBoxLayout()
        self.set_layout.addLayout(start_box)
        self.set_layout.addLayout(player_box)
        self.set_layout.addLayout(mplier_box)
        self.set_layout.addLayout(begin_box)
        self.set_layout.addLayout(level_labels_box)
        self.set_layout.addLayout(self.preview_box)
        # self.set_layout.addWidget(self.begin_btn)
        self.set_layout.addStretch(1)

        lbl_box = QHBoxLayout()
        lbl_box.addWidget(lbl2)
        lbl_box.addWidget(self.lbl)
        lbl_box.addStretch(1)

        btn_box = QHBoxLayout()
        btn_box.addWidget(self.btn1)
        btn_box.addWidget(self.btn2)
        btn_box.addLayout(lbl_box)
        btn_box.addStretch(1)

        # tbl_box = QHBoxLayout()
        # tbl_box.addWidget(self.tbl)

        self.play_layout = QVBoxLayout()
        self.play_layout.addLayout(btn_box)
        # self.play_layout.addLayout(tbl_box)
        self.play_layout.addStretch(1)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.set_layout)
        self.layout.addLayout(self.play_layout)
        # self.layout.removeItem(self.set_layout)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
        self.setGeometry(300, 300, 900, 600)
        self.setMinimumSize(900, 600)
        self.setWindowTitle('Baccarat')
        self.show()

    # noinspection PyTypeChecker
    def update_preview(self):
        base_row = [1, 1, 1, 2, 2, 4, 6, 10, 16, 26]
        c = self.starting_bet.value()
        rows = []
        for j in range(3):
            row = [i * c * self.mplier.value() ** j for i in base_row]
            row = [round(i, 2) for i in row]
            rows += row

        child_num = self.preview_box.count()
        for i in range(10, child_num):
            item = self.preview_box.itemAt(i).widget()
            print(item.text())
            # print(type(item))
            # print('i:', i)
            # print('i:', str(i))
            # print(str(rows[i - 10]))
            item.setText(str(rows[i - 10]))

        print('bet:', c, 'mplier:', self.mplier.value())

    def begin(self):
        # self.starting_bet, self.p_num, self.mplier
        starting_bet, p_num, mplier = self.starting_bet.value(), self.p_num.value(), self.mplier.value()

        print('the values are:', starting_bet, p_num, mplier)
        print('types:', type(starting_bet), type(p_num), type(mplier))

        factory = GameFactory(num_p=p_num, multiplier=mplier, starting_bet=starting_bet)
        _, self.game = factory.create()

        # GameFactory should be instanced before this
        hlabels = ['partner', 'play', 'level', 'index', 'bet', 'result', 'target', 'net']
        vlabels = [gambler.name for gambler in self.game.gamblers]
        self.tbl = QTableWidget(len(vlabels), len(hlabels))
        self.tbl.setHorizontalHeaderLabels(hlabels)
        self.tbl.setVerticalHeaderLabels(vlabels)
        # self.tbl.setMaximumHeight(355)
        self.tbl.setMinimumHeight(355)
        tbl_box = QHBoxLayout()
        tbl_box.addWidget(self.tbl)
        self.play_layout.addLayout(tbl_box)
        # ^ TODO: move table creation in a separate function

        self.starting_bet.setDisabled(True)
        self.p_num.setDisabled(True)
        self.mplier.setDisabled(True)
        self.begin_btn.setDisabled(True)
        self.btn1.setDisabled(False)
        self.btn2.setDisabled(False)

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
            # row[-1] = floor(row[-1]*100)/100
            # row[-1] = round(row[-1], 2)
            data.append(row)

        # data[-1][-3] = round(data[-1][-3], 1)

        for i in range(len(data)):
            for j in range(len(data[i])):
                self.tbl.setItem(i, j, QTableWidgetItem(str(data[i][j])))



