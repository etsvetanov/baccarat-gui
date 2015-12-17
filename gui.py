__author__ = 'etsvetanov'
from math import floor
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QLabel, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QHBoxLayout, QFrame, QDoubleSpinBox,
                             QSpinBox, QGridLayout)

from factory import GameFactory
from core import roll
import pyqtgraph as pg


class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.game = None
        self.display_lbl = None
        self.tbl = None
        self.player_btn = None
        self.bank_btn = None
        self.play_layout = None
        self.settings_layout = None
        self.layout = None
        self.starting_bet = None
        self.p_num = None
        self.mplier = None
        self.begin_btn = None
        self.preview_box = None
        self.sim_btn = None
        self.sim_layout = None
        self.sim_widget = None
        self.collector = None
        self.initUI()

    def settingsUI(self):
        """this function creates the initial settings UI"""

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
        self.p_num.setRange(1, 10)
        self.p_num.setMinimumHeight(50)
        self.p_num.setMinimumWidth(120)
        # -----------------------------------
        mplier_lbl = QLabel('Step')
        self.mplier = QSpinBox()
        self.mplier.setRange(2, 10)
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
        # -----------------------------------
        self.sim_btn = QPushButton('Simulate')
        self.sim_btn.clicked.connect(self.simulate)
        self.sim_btn.setMinimumWidth(100)
        self.sim_btn.setMinimumHeight(50)
        sim_lbl = QLabel('')

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

        siim_btn_box = QVBoxLayout()
        siim_btn_box.addWidget(sim_lbl)
        siim_btn_box.addWidget(self.sim_btn)

        level_labels_box = self.previewUI()
        self.settings_layout = QHBoxLayout()
        self.settings_layout.addLayout(start_box)
        self.settings_layout.addLayout(player_box)
        self.settings_layout.addLayout(mplier_box)
        self.settings_layout.addLayout(begin_box)
        self.settings_layout.addLayout(siim_btn_box)
        self.settings_layout.addLayout(level_labels_box)
        self.settings_layout.addLayout(self.preview_box)
        self.settings_layout.addStretch(1)

    def previewUI(self):
        self.preview_box = QGridLayout()

        for i in range(4):
            for j in range(10):
                label = QLabel('[' + str(j) + ']')
                self.preview_box.addWidget(label, i, j)

        level_labels_box = QGridLayout()
        level_labels_box.addWidget(QLabel(''), 0, 0)
        for i in range(1, 4):
            label = QLabel('Level' + str(i))
            level_labels_box.addWidget(label, i, 0)

        self.update_preview()
        
        return level_labels_box
        
    def playUI(self):
        self.player_btn = QPushButton("Player")
        self.bank_btn = QPushButton("Bank")
        self.calc_btn = QPushButton("Calculate")
        self.player_btn.clicked.connect(self.button_clicked)
        self.bank_btn.clicked.connect(self.button_clicked)
        self.calc_btn.clicked.connect(self.calculate)

        for btn in [self.player_btn, self.bank_btn, self.calc_btn]:
            btn.setMinimumWidth(100)
            btn.setMinimumHeight(70)
            btn.setDisabled(True)

        self.display_lbl = QLabel('  $0')
        self.display_lbl.setFrameShape(QFrame.WinPanel)
        self.display_lbl.setFrameShadow(QFrame.Sunken)
        self.display_lbl.setMinimumHeight(30)
        self.display_lbl.setMinimumWidth(160)
        self.display_lbl.setStyleSheet("""
                        .QLabel {
                            color: red;
                            font-size: 20px
                        }
                    """)

        bet_lbl = QLabel('Bet: ')

        """----- Layouts ------"""
        """ there is one main layout - VBox - layout """
        """ and three sub-main layouts - settings_layout, play_layout and sim_layout"""
        """ everything else is a sub layout to these"""

        lbl_box = QHBoxLayout()
        lbl_box.addWidget(bet_lbl)
        lbl_box.addWidget(self.display_lbl)
        lbl_box.addStretch(1)

        btn_box = QHBoxLayout()
        btn_box.addWidget(self.player_btn)
        btn_box.addWidget(self.bank_btn)
        btn_box.addLayout(lbl_box)
        btn_box.addWidget(self.calc_btn)
        btn_box.addStretch(1)

        self.play_layout = QVBoxLayout()
        self.play_layout.addLayout(btn_box)
        self.play_layout.addStretch(1)

    def initUI(self):
        self.settingsUI()  # return settings_layout ?

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.settings_layout)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
        self.setGeometry(300, 300, 900, 600)
        self.setMinimumSize(900, 600)
        self.setWindowTitle('Baccarat')
        self.show()

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
            item.setText(str(rows[i - 10]))

    def begin(self):
        self.playUI()
        self.layout.addLayout(self.play_layout)
        self.play_layout.addLayout(self.create_table())

        self.disable_settings_ui()
        self.calc_btn.setDisabled(False)

    def simulate(self):
        self.disable_settings_ui()
        self.create_game()
        self.simulateUI()
        # simulate N number of plays
        n = 1000
        for i in range(n):
            self.game.set_outcome()

        self.create_graph(n)

    def create_graph(self, n):
        plot_item = self.sim_widget.getPlotItem()
        xVals = [i for i in range(1, n + 1)]
        # yVals = [round[] for round in self.collector.player_data['RealPlayer']]

    def simulateUI(self):

        self.sim_widget = pg.PlotWidget()
        sim_box = QVBoxLayout()
        sim_box.addWidget(self.sim_widget)
        sim_box.addStretch(1)
        self.layout.addLayout(sim_box)

        # plot_item.plot([1, 2, 3, 4, 5], [7, 6, 7, 8, 6], pen='r')

    def disable_settings_ui(self):
        self.starting_bet.setDisabled(True)
        self.p_num.setDisabled(True)
        self.mplier.setDisabled(True)
        self.begin_btn.setDisabled(True)
        self.sim_btn.setDisabled(True)

    def create_game(self):
        starting_bet, num_p, mplier = self.starting_bet.value(), self.p_num.value(), self.mplier.value()

        factory = GameFactory(num_p=num_p, multiplier=mplier, starting_bet=starting_bet)
        self.collector, self.game = factory.create()

    def create_table(self):
        self.create_game()

        # GameFactory should be instanced before this moment
        hlabels = ['partner', 'play', 'level', 'index', 'bet', 'result', 'target', 'net']
        vlabels = [gambler.name for gambler in self.game.gamblers]
        self.tbl = QTableWidget(len(vlabels), len(hlabels))
        self.tbl.setHorizontalHeaderLabels(hlabels)
        self.tbl.setVerticalHeaderLabels(vlabels)
        self.tbl.setMinimumHeight(700)
        tbl_box = QHBoxLayout()
        tbl_box.addWidget(self.tbl)

        return tbl_box

    def button_clicked(self):
        self.player_btn.setDisabled(True)
        self.bank_btn.setDisabled(True)
        self.calc_btn.setDisabled(False)
        sender = self.sender()
        self.game.set_outcome(sender.text().lower())
        self.populate_table()

    def calculate(self):
        self.player_btn.setDisabled(False)
        self.bank_btn.setDisabled(False)
        self.calc_btn.setDisabled(True)
        self.game.deal()
        self.populate_table()
        p = self.game.gamblers[-1]
        self.display_lbl.setText('  $' + str(p.bet_size) + ' on ' + p.bet_choice.upper())

    def populate_table(self):
        data = []
        for g in self.game.gamblers:
            row = self.game.cltr.player_data[g.name][-1]
            data.append(row)

        for i in range(len(data)):
            for j in range(len(data[i])):
                self.tbl.setItem(i, j, QTableWidgetItem(str(data[i][j])))



