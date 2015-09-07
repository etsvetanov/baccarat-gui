import plotly.plotly as py
import plotly.tools as tls

from plotly.graph_objs import *
from random import randint
from openpyxl import Workbook


def print_header():
    print('{:>3} {:>6} {:>4} {:>5} {:>5} {:>6}'.format(
        'i',
        'd_up',
        'bet',
        'level',
        'res',
        'net'))


def roll():
    n = randint(0, 1)  # player : bank ratio is not exactly 50:50!
    if n == 1:
        return 'player'
    else:
        return 'bank'


class Game():
    def __init__(self, store_data=False):
        self.gamblers = []
        self.outcome = None
        self.store_data = store_data
        if store_data:
            self.wb_created = False
            self.wb = Workbook()
            self.ws = self.wb.active

    def create_spreadsheet(self):
        self.ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=2)
        self.ws['A1'] = 'Casino'
        for j in range(len(self.gamblers)):
            self.ws.merge_cells(start_row=1, start_column=3+(4*j), end_row=1, end_column=6+(4*j))
            c = self.ws.cell(row=1, column=3+(4*j))
            c.value = self.gamblers[j].name

        columns = ['play', 'bet', 'outcome', 'net']
        row_list = [column for x in range(len(self.gamblers)) for column in columns]
        row_list.insert(0, 'outcome')
        row_list.insert(0, 'game')
        print(row_list)
        self.ws.append(row_list)
        self.wb.save('test.xlsx')

    @staticmethod
    def roll():
        n = randint(0, 1)  # player : bank ratio is not exactly 50:50!
        if n == 1:
            return 'player'
        else:
            return 'bank'

    def register(self, gamblers):  # player objects
        self.outcome = None
        self.gamblers = gamblers
        self.run()

    def run(self):
        assert self.gamblers is not None

        for gambler in self.gamblers:
            gambler.play()

        self.outcome = self.roll()
        self.notify_observers()

    def notify_observers(self):
        assert self.outcome is not None

        for gambler in self.gamblers:
            if gambler.bet_choice == self.outcome:
                amount = gambler.bet_size * 2
                gambler.update(outcome='win', reward=amount)
            else:
                gambler.update(outcome='loss')

    def plotz(self):
        py.sign_in(username='etsvetanov', api_key='nsyswe1pg2')
        traces = []
        num_of_rounds = len(self.gamblers[0].net_list)
        x = [i for i in range(num_of_rounds)]

        for gambler in self.gamblers:
            trace = Scatter(name=gambler.name, x=x, y=gambler.net_list)
            traces.append(trace)

        y_net_list = [trace['y'] for trace in traces]
        y_net_total = [sum(amounts) for amounts in zip(*y_net_list)]
        total_trace = Scatter(name='Total', x=x, y=y_net_total)
        traces.append(total_trace)
        data = Data(traces)
        unique_url = py.plot(data, filename='graph')

    def write_xl(self):
        if not self.wb_created:
            self.create_spreadsheet()
            self.wb_created = True


class BaseStrategy():
    def __init__(self, coefficient=1):
        base_row = [1, 1, 1, 2, 2, 4, 6, 10, 16, 26]
        self.c = coefficient
        self.row = [i * self.c for i in base_row]
        self.i = 0
        self.double_up = False
        self.outcome = 'loss'
        self.level = 1
        self.level_target = 0  # drop to lower leve l after this gets to (sum(self.row) * level ) / 2
        self.last_index = 0

    def update(self, outcome, reward=None):
        self.outcome = outcome
        self.update_index()
        self.is_double()

        if reward:
            self.level_target += reward
            self.update_level()

    def update_level(self, increase=False):
        if increase:
            self.level += 1
            self.level_target = 0
        elif self.level_target >= ((sum(self.row) * (2 ** (self.level - 1))) / 2):
            self.level -= 1
            self.level_target = 0
        else:
            pass

        if self.level < 1:
            self.level = 1

    def update_index(self):
        self.last_index = self.i  # we are remembering the last index before calculating the new one

        if self.outcome == 'loss':
            self.i += 1
        elif self.i == 3 or self.i >= 5:
            self.i -= 3
        else:  # if self.i <= 2 or self.i == 4 AND last_outcome == 'w'
            if self.double_up:
                self.i = 0  # this is after we've played double bet and won -> we must go to 0

        if self.i >= len(self.row):  # if we loose all go to [0] 
            self.i = 0
            self.update_level(increase=True)
            # self.level += 1  # or self.level *= 2 ... linear or geometric
        assert 0 <= self.i < len(self.row)

    def is_double(self):
        # self.double_up is going to be used in THIS play
        if (self.i <= 2 or self.i == 4) and self.last_index == self.i and self.double_up is False:
            self.double_up = True
        elif self.double_up:  # if double_up was True till now
            self.double_up = False

    def get_bet_size(self):  # res - result
        bet = 0
        level_multiplier = 2 ** (self.level - 1)

        if self.double_up:
            bet = self.row[self.i] * level_multiplier * 2  # or make double_up int and multiply by it
        else:
            bet = self.row[self.i] * level_multiplier

        assert bet > 0
        self.level_target -= bet

        return bet

    @staticmethod
    def get_bet_choice():
        choice = roll()
        return choice


class Player():
    def __init__(self, strategy, name):
        self.name = name
        self.strategy = strategy
        self.bet_size = None
        self.bet_choice = None
        self.statistics = {'net': 0, 'won': 0, 'lost': 0, 'largest_bet': 0}
        self.res = 'loss'
        self.net_list = []

    def print_turn(self):
        print('{:>3} {:>6} {:>4} {:>5} {:>5} {:>6}'.format(
            self.strategy.i,
            str(self.strategy.double_up),
            self.bet_size,
            self.strategy.level,
            self.res,
            self.statistics['net']))

    def update(self, outcome, reward=None):
        self.res = outcome

        if reward:
            self.statistics['won'] += 1
            assert reward is not None
            self.statistics['net'] += reward
        else:
            self.statistics['lost'] += 1

        self.print_turn()
        self.net_list.append(self.statistics['net'])

        self.strategy.update(outcome, reward)

    def bet(self, amount):
        if amount > self.statistics['largest_bet']:
            self.statistics['largest_bet'] = amount

        self.statistics['net'] -= amount

    def play(self):
        self.bet_size = self.strategy.get_bet_size()
        self.bet_choice = self.strategy.get_bet_choice()
        assert self.bet_size is not None
        assert self.bet_choice is not None

        self.bet(self.bet_size)  # this can actually be called without arguments


strat1 = BaseStrategy()
strat2 = BaseStrategy()
p1 = Player(strategy=strat1, name='p1')
p2 = Player(strategy=strat2, name='p2')
table = Game(store_data=True)
players = [p1, p2]

print_header()

for i in range(10):
    table.register(players)
table.plotz()
table.write_xl()

print('Statistics:')
print('plays won:   ', p1.statistics['won'])
print('plays lost:  ', p1.statistics['lost'])
print('largest bet: ', p1.statistics['largest_bet'])
