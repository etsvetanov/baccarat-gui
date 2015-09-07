from random import randint
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *


def roll():
    n = randint(0, 1)
    if n == 1:
        return 'p'
    else:
        return 'b'


class BaseStrategy():
    def __init__(self):
        # 0  1  2  3  4  5  6   7   8   9
        self.row = [2, 2, 2, 4, 4, 8, 12, 20, 32, 52]
        self.i = 0  # row index position
        self.double_up = False
        self.last_index = -1  # ??

    def get_index(self, last_outcome):

        if last_outcome == 'l':
            self.i += 1
        elif self.i == 3 or self.i >= 5:
            self.i -= 3
        else:  # if self.i <= 2 or self.i == 4 AND last_outcome == 'w'
            if self.double_up:
                self.i = 0  # this is after we've played double bet and won -> we must go to 0
        if self.i >= len(self.row):  # if we loose all go to [0] 
            self.i = 0
        assert 0 <= self.i < len(self.row)

    def is_double(self):
        # self.double_up is going to be used in THIS play

        if self.i <= 2 or self.i == 4:
            if self.last_index == self.i and self.double_up == False:  # if double_up was False till now
                self.double_up = True
            elif self.double_up == True:  # if double_up was True till now
                self.double_up = False

    def get_bet_size(self):  # res - result
        bet = 0
        self.is_double()
        if self.double_up:
            bet = self.row[self.i] * 2  # or make double_up int (1 or 2) and multiply by it
        else:
            bet = self.row[self.i]

        self.last_index = self.i
        assert bet > 0
        return bet


class Player():
    def __init__(self, strategy):
        self.strategy = strategy
        self.net = 0
        self.res = 'l'

    def bet(self, amount):
        self.net -= amount

        outcome = roll()
        if outcome == 'p':
            self.res = 'w'
            self.net += 2 * amount
        else:
            self.res = 'l'

        print('{:>3} {:>6} {:>4} {:>3} {:>6}'.format(
            self.strategy.i,
            str(self.strategy.double_up),
            amount,
            self.res,
            self.net))
        self.strategy.get_index(self.res)

    def play(self, num_hands):
        data_x = []
        data_y = []
        for i in range(num_hands):
            self.bet(self.strategy.get_bet_size())
            data_x.append(i)
            data_y.append(self.net)

        return data_x, data_y


strat = BaseStrategy()
p1 = Player(strat)

print('{:>3} {:>6} {:>4} {:>3} {:>6}'.format(
    'i',
    'd_up',
    'bet',
    'res',
    'net'))

x, y = p1.play(100000)


py.sign_in('etsvetanov', 'nsyswe1pg2')
stream_id = '7dmuy3q0sd'
stream = Stream(token=stream_id, maxpoints=1000)
trace1 = Scatter(x=[], y=[], stream=stream)
data = Data([trace1])
layout = Layout(title='Graphz')
fig = Figure(data=data, layout=layout)
unique_url = py.plot(fig, filename='stream')
py.plot(data)
s = py.Stream(stream_id)
s.write(dict(x=1, y=2))
s.close()

