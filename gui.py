from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QLabel, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QHBoxLayout, QFrame, QDoubleSpinBox,
                             QSpinBox, QGridLayout, QProgressBar, qApp, QCheckBox,
                             QDialog, QComboBox, QStyledItemDelegate)

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from factory import GameFactory
from data_visualization import SpreadSheet
import strategies
import inspect
import pyqtgraph as pg

COLUMNS = 'columns'


class BigButton(QPushButton):
    def __init__(self, text):
        QPushButton.__init__(self, text)
        self.setMinimumWidth(100)
        self.setMinimumHeight(50)


class BigSpinBox(QSpinBox):
    def __init__(self):
        QSpinBox.__init__(self)
        self.setMinimumWidth(100)
        self.setMinimumHeight(50)


class BigDoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        QDoubleSpinBox.__init__(self)
        self.setMinimumHeight(50)
        self.setMinimumWidth(120)
        self.setMaximumHeight(50)
        self.setMaximumWidth(120)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.options_dic = {}

        self.game = None
        self.display_lbl = None
        self.tbl = None
        self.calc_btn = None
        self.player_btn = None
        self.bank_btn = None
        self.play_layout = None
        self.settings_layout = None
        self.layout = None
        self.starting_bet = 0.01
        self.p_num = 1
        self.mplier = 2
        self.begin_btn = None
        self.preview_box = None
        self.sim_btn = None
        self.sim_layout = None
        self.sim_widget = None
        self.collector = None
        self.round_num = None
        self.go_btn = None
        self.round_prog_bar = None
        self.sheet_tick = None
        self.options_btn = None
        self.columns = None
        self.initUI()


    @staticmethod
    def create_generic_button_box(name, callback=None, add_label=True, label_name=''):
        """
        :param name: Button name
        :param callback: Slot to connect to "clicked" signal
        :param add_label: If True a label will be added to the layout
        :param label_name: Will be used as the label name, default is empty string
        :return: generated layout and button references
        """
        lbl = None
        btn = BigButton(name)
        if callback is not None:
            btn.clicked.connect(callback)

        if add_label is True:
            lbl = QLabel(label_name)

        layout = QVBoxLayout()
        if lbl is not None:
            layout.addWidget(lbl)

        layout.addWidget(btn)

        return layout, btn

    def settingsUI(self):
        """this function creates the initial settings UI"""

        options_box, self.options_btn = self.create_generic_button_box('Options', self.options)
        begin_box, self.begin_btn = self.create_generic_button_box('Begin', self.begin)
        sim_box, self.sim_btn = self.create_generic_button_box('Simulate', self.simulate)

        self.settings_layout = QHBoxLayout()
        self.settings_layout.addLayout(options_box)
        self.settings_layout.addLayout(begin_box)
        self.settings_layout.addLayout(sim_box)
        self.settings_layout.addLayout(self.preview_box)
        self.settings_layout.addStretch(1)

    def playUI(self):
        self.player_btn = BigButton("Player")
        self.bank_btn = BigButton("Bank")
        self.calc_btn = BigButton("Calculate")
        self.player_btn.clicked.connect(self.choice_button_clicked)
        self.bank_btn.clicked.connect(self.choice_button_clicked)
        self.calc_btn.clicked.connect(self.calculate)

        for btn in [self.player_btn, self.bank_btn, self.calc_btn]:
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

    def init_options(self):
        self.options_dic[COLUMNS] = {}
        self.columns = ['partner', 'play', 'level', 'index', 'bet', 'result', 'target', 'net']
        self.options_dic[COLUMNS]['partner'] = False
        self.options_dic[COLUMNS]['play'] = False
        self.options_dic[COLUMNS]['level'] = True
        self.options_dic[COLUMNS]['index'] = True
        self.options_dic[COLUMNS]['bet'] = False
        self.options_dic[COLUMNS]['result'] = False
        self.options_dic[COLUMNS]['target'] = True
        self.options_dic[COLUMNS]['net'] = True

    def initUI(self):
        self.settingsUI()  # return settings_layout ?
        self.init_options()

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.settings_layout)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
        self.setGeometry(300, 300, 900, 600)
        self.setMinimumSize(900, 600)
        self.setWindowTitle('Baccarat')
        self.show()

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

    def create_graph(self, n):
        plot_item = self.sim_widget.getPlotItem()
        plot_item.setLabel('left', text='Net')
        plot_item.setLabel('bottom', text='Round')
        xVals = [i for i in range(1, n + 1)]
        yVals = [round[7] for round in self.collector.player_data['RealPlayer']]

        plot_item.plot(xVals, yVals, pen='r')

    def go(self):
        self.go_btn.setDisabled(True)
        n = self.round_num.value()
        self.round_prog_bar.setMaximum(n)
        for i in range(n):
            self.round_prog_bar.setValue(i+1)
            self.game.deal()
            self.game.set_outcome()
            qApp.processEvents()  # I have no idea what this does but it's working! see: http://stackoverflow.com/questions/21886260/python-ui-gets-unresponsive-after-long-run

        self.create_graph(n)

        qApp.processEvents()  # wadap
        if self.sheet_tick.isChecked():
            sh = SpreadSheet(self.game.cltr)
            sh.create_spreadsheet()

    def simulateUI(self):
        self.sim_widget = pg.PlotWidget()

        round_num_lbl = QLabel('Number of rounds')
        self.round_num = QSpinBox()
        self.round_num.setRange(100, 1000000)
        self.round_num.setMinimumHeight(50)
        self.round_num.setMinimumWidth(120)
        self.round_num.setSingleStep(1000)
        round_num_box = QVBoxLayout()
        round_num_box.addWidget(round_num_lbl)
        round_num_box.addWidget(self.round_num)
        # ------
        go_lbl = QLabel('')
        self.go_btn = BigButton('Go')
        self.go_btn.clicked.connect(self.go)
        go_box = QVBoxLayout()
        go_box.addWidget(go_lbl)
        go_box.addWidget(self.go_btn)
        # ------
        # sheet_lbl = QLabel('Create spreadsheet')
        # sheet_lbl.setAlignment(Qt.AlignTop)
        self.sheet_tick = QCheckBox('Create spreadsheet')

        sheet_tick_box = QVBoxLayout()
        # sheet_tick_box.addWidget(sheet_lbl)
        sheet_tick_box.addWidget(self.sheet_tick)
        # ------
        prog_bar_lbl = QLabel('Progess')
        # prog_bar_lbl.setAlignment(Qt.AlignBottom)
        self.round_prog_bar = QProgressBar()
        self.round_prog_bar.setMinimumHeight(50)
        # self.round_prog_bar.setMinimumWidth(200)
        prog_bar_box = QVBoxLayout()
        prog_bar_box.addWidget(prog_bar_lbl)
        prog_bar_box.addWidget(self.round_prog_bar)
        # ------
        sim_settings_box = QHBoxLayout()
        sim_settings_box.addLayout(round_num_box)
        sim_settings_box.addLayout(sheet_tick_box)
        sim_settings_box.addLayout(go_box)
        sim_settings_box.addLayout(prog_bar_box)

        sim_box = QVBoxLayout()
        sim_box.addLayout(sim_settings_box)  # its a layout not a widget!
        sim_box.addWidget(self.sim_widget)
        sim_box.addStretch(1)

        self.layout.addLayout(sim_box)

    def disable_settings_ui(self):
        self.options_btn.setDisabled(True)
        self.begin_btn.setDisabled(True)
        self.sim_btn.setDisabled(True)

    def create_game(self):
        starting_bet, num_p, mplier = self.starting_bet, self.p_num, self.mplier

        factory = GameFactory(num_p=num_p, multiplier=mplier, starting_bet=starting_bet)
        self.collector, self.game = factory.create(self.columns)

    def create_table(self):
        self.create_game()

        # GameFactory should be instantiated before this moment!
        hlabels = [column for column in self.columns
                   if self.options_dic[COLUMNS][column] == True]
        vlabels = [gambler.name for gambler in self.game.gamblers]
        self.tbl = QTableWidget(len(vlabels), len(hlabels))
        self.tbl.setHorizontalHeaderLabels(hlabels)
        self.tbl.setVerticalHeaderLabels(vlabels)
        self.tbl.setMinimumHeight(700)
        tbl_box = QHBoxLayout()
        tbl_box.addWidget(self.tbl)

        return tbl_box

    def choice_button_clicked(self):
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
            row_data = self.game.cltr.player_data[g.name][-1]
            row = [row_data[i] for i in range(len(row_data))
                   if self.options_dic[COLUMNS][self.columns[i]] == True]
            data.append(row)

        for i in range(len(data)):
            for j in range(len(data[i])):
                self.tbl.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    def options(self):
        a = OptionsDialog(self)
        result = a.exec()


class OptionsDialog(QDialog):
    def __init__(self, main_window):
        # todo: try to replace .main reference with .parent
        super().__init__()

        self.main = main_window
        self.options_dic = main_window.options_dic
        self.layout = None
        self.starting_bet = None
        self.p_num = None
        self.mplier = None
        self.preview_box = None
        self.strategy_choice = None
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # ---------------------------------------
        strategy_box = self.create_box_strategy()
        box_mplier = self.create_box_mplier()
        box_p_num = self.create_box_p_num()
        box_starting_bet = self.create_box_starting_bet()
        box_preview = self.create_box_preview()

        param_spin_box = QVBoxLayout()
        param_spin_box.addLayout(box_mplier)
        param_spin_box.addLayout(box_p_num)
        param_spin_box.addLayout(box_starting_bet)
        param_spin_box.addStretch(1)

        param_box = QHBoxLayout()
        param_box.addLayout(param_spin_box)
        param_box.insertSpacing(1, 30)
        param_box.addLayout(box_preview)
        # param_box.addStretch(1)
        self.layout.addLayout(strategy_box)
        self.layout.addLayout(param_box)
        # ----------------------------------------
        self.create_box_columns_options()
        ok_box = self.create_box_ok()
        self.layout.addLayout(ok_box)

        self.layout.addStretch(1)
        self.setLayout(self.layout)

        self.setGeometry(300, 300, 550, 600)
        self.setMinimumSize(550, 600)

    def create_box_starting_bet(self):
        start_lbl = QLabel('Starting bet')
        self.starting_bet = BigDoubleSpinBox()
        self.starting_bet.setRange(0.01, 100)
        self.starting_bet.setValue(self.main.starting_bet)
        self.starting_bet.setSingleStep(0.1)
        self.starting_bet.valueChanged.connect(self.update_preview)

        start_box = QVBoxLayout()
        start_box.addWidget(start_lbl)
        start_box.addWidget(self.starting_bet)

        # self.layout.addLayout(start_box)
        return start_box

    def create_box_p_num(self):
        p_num_lbl = QLabel('Number of pairs')
        self.p_num = BigDoubleSpinBox()
        self.p_num.setRange(1, 10)
        self.p_num.setValue(self.main.p_num)
        self.p_num.valueChanged.connect(self.update_preview)
        self.p_num.valueChanged.connect(lambda: self.update_parameter('p_num'))

        player_box = QVBoxLayout()
        player_box.addWidget(p_num_lbl)
        player_box.addWidget(self.p_num)
        player_box.addStretch(1)

        # self.layout.addLayout(player_box)
        return player_box

    def create_box_mplier(self):
        mplier_lbl = QLabel('Step')
        self.mplier = BigDoubleSpinBox()
        self.mplier.setRange(2, 10)

        self.mplier.setValue(self.main.mplier)
        self.mplier.valueChanged.connect(self.update_preview)
        self.mplier.valueChanged.connect(lambda: self.update_parameter('mplier'))
        self.mplier.setToolTip('The starting bet is multiplied by this value for each consecutive level')

        mplier_box = QVBoxLayout()
        mplier_box.addWidget(mplier_lbl)
        mplier_box.addWidget(self.mplier)

        # self.layout.addLayout(mplier_box)
        return mplier_box

    def update_parameter(self, target):
        value = self.sender().value()
        setattr(self.main, target, int(value))

    def create_box_strategy(self):
        ls = [m[0] for m in inspect.getmembers(strategies, inspect.isclass)]  # if m[1].__module__ == 'strategies']

        self.strategy_choice = QComboBox()
        font = QFont()
        font.setPointSize(font.pointSize() + 10)
        self.strategy_choice.setFont(font)

        self.strategy_choice.highlighted[str].connect(self.strategy_selected)
        for i, strat in enumerate(strategies.REGISTRY):
            self.strategy_choice.insertItem(i, strat)

        strategy_box = QHBoxLayout()
        strategy_box.addWidget(self.strategy_choice)
        strategy_box.addStretch(1)
        return strategy_box

    def strategy_selected(self, strategy):
        print(strategy)
        pass

    def create_box_columns_options(self):

        columns_layout = QVBoxLayout()
        columns_lbl = QLabel('Columns')
        columns_layout.addWidget(columns_lbl)

        for column, enabled in sorted(self.options_dic['columns'].items()):
            check_box = QCheckBox(column)
            check_box.setChecked(enabled)
            check_box.clicked.connect(self.set_option)
            columns_layout.addWidget(check_box)

        self.layout.addLayout(columns_layout)

    @pyqtSlot(bool)
    def set_option(self, enabled):
        column = self.sender().text()
        self.options_dic['columns'][column] = enabled
        print(1)

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

    def create_box_ok(self):
        ok_btn = BigButton('Ok')
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        ok_box = QHBoxLayout()
        ok_box.addWidget(ok_btn)
        ok_box.addStretch(1)

        return ok_box
        # self.layout.addLayout(ok_box)

    def create_box_preview(self):
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

        container_box = QHBoxLayout()
        container_box.addLayout(level_labels_box)
        container_box.addLayout(self.preview_box)
        container_box.addStretch(1)
        some_vertical_box = QVBoxLayout()
        some_vertical_box.addLayout(container_box)
        some_vertical_box.addStretch(1)
        return some_vertical_box
