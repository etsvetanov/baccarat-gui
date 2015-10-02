import plotly.plotly as py

from plotly.graph_objs import Scatter, Data
from random import randint


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
    def __init__(self, gamblers, cltr=None, max_rounds=1000):
        self.max_rounds = max_rounds
        self.round = 0
        self.gamblers = gamblers
        self.outcome = None
        self.cltr = cltr

    @staticmethod
    def roll():
        n = randint(0, 1)  # player : bank ratio is not exactly 50:50!
        if n == 1:
            return 'player'
        else:
            return 'bank'

    def add(self, gambler):  # player objects
        # THIS WILL NOT WORK!
        self.outcome = None
        self.gamblers.append(gambler)
        self.run()

    def remove(self, gambler):
        self.gamblers.remove(gambler)

    def submit_data(self):
        self.cltr.push_game_data([self.round, self.outcome])

    def run(self, rounds):
        self.max_rounds = rounds
        while self.gamblers and self.round <= self.max_rounds:
            self.deal()

    def deal(self, outcome=None):

        print('Round:', self.round)
        self.round += 1
        for gambler in self.gamblers:
            gambler.play()
        # print(outcome)

        if outcome:
            self.outcome = outcome
        else:
            self.outcome = self.roll()

        if self.cltr:
            self.submit_data()

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
        print('plotting the results...')
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


class BaseStrategy():
    def __init__(self, coefficient=1):
        base_row = [1, 1, 1, 2, 2, 4, 6, 10, 16, 26]
        self.c = coefficient
        self.row = [i * self.c for i in base_row]
        self.i = 0
        self.double_up = False
        self.outcome = 'loss'
        self.level = 1
        self.level_target = 0  # drop to lower level after this gets to (sum(self.row) * level ) / 2
        self.last_index = 0

    def update(self, outcome, reward=None):
        self.outcome = outcome
        self.update_index()
        self.is_double()

        if reward:
            self.level_target += reward
            self.update_level()

    def update_level(self, increase=False):
        """
        go to a higher level if you loose the last bet in the row
        or go to a lower level if you win a amount equal to the
        sum of the bets in the previous level row
        """
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


class PairStrategy(BaseStrategy):
    def __init__(self, coefficient=1):
        self.lead = False
        BaseStrategy.__init__(self, coefficient)
        self.pair = None

    def set_pair(self, pair):
        self.pair = pair

    def get_bet_choice(self):
        if self.pair.strategy.lead:
            self.pair.strategy.lead = False
            if self.pair.bet_choice == 'player':
                return 'bank'
            else:
                return 'player'
        else:
            self.lead = True
            choice = roll()
            return choice


class Player():
    def __init__(self, strategy, name, cltr=None):
        self.cltr = cltr
        self.name = name
        self.strategy = strategy
        self.bet_size = 0
        self.bet_choice = None
        self.statistics = {'net': 0, 'won': 0, 'lost': 0, 'largest_bet': 0}
        self.res = 'loss'
        self.net_list = []
        self.table = None

    def print_turn(self):
        print('{:>15} {:>3} {:>6} {:>4} {:>5} {:>5} {:>6}'.format(
            self.name,
            self.strategy.i,
            str(self.strategy.double_up),
            self.bet_size,
            self.strategy.level,
            self.res,
            self.statistics['net']))

    def join(self, table):
        table.add(self)
        self.table = table

    def submit_data(self):
        data = [self.bet_choice, self.strategy.level, self.strategy.i,
                str(self.bet_size) if not self.strategy.double_up else '2*' + str(int(self.bet_size / 2)),
                self.res, self.statistics['net']]
        self.cltr.push_player_data(self.name, data)

    def update(self, outcome, reward=None):
        self.res = outcome
        if reward:
            self.statistics['won'] += 1
            assert reward is not None
            self.statistics['net'] += reward
        else:
            self.statistics['lost'] += 1

        if self.cltr:
            self.submit_data()

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


class OverseerStrategy(BaseStrategy):
    """
    This strategy is ment to be used on the Overseer class
    """
    def __init__(self, coefficient=1, minions=None):
        self.minions = minions
        BaseStrategy.__init__(self, coefficient)
        self.calculated = False
        self.bet_size = 0
        self.bet_choice = None
        self.__last_index = '-'

    @property
    def last_index(self):
        return '-'

    @last_index.setter
    def last_index(self, last_i):
        pass

    def calculate(self):
        minion_bets = {'player': 0, 'bank': 0}
        for minion in self.minions:
            minion_bets[minion.bet_choice] += minion.bet_size

        if minion_bets['player'] > minion_bets['bank']:
            self.bet_size, self.bet_choice = minion_bets['player'] - minion_bets['bank'], 'player'
        elif minion_bets['bank'] > minion_bets['player']:
            self.bet_size, self.bet_choice = minion_bets['bank'] - minion_bets['player'], 'bank'
        else:
            self.bet_size, self.bet_choice = 0, 'tie'

    def get_bet_choice(self):
        if self.calculated:
            self.calculated = False
            return self.bet_choice
        else:
            self.calculate()
            self.calculated = True
            return self.bet_choice

    def get_bet_size(self):
        if self.calculated:
            self.calculated = False
            return self.bet_size
        else:
            self.calculate()
            self.calculated = True
            return self.bet_size


class Overseer(Player):
    """
    This class represents a player that calculates bets depending on the other players bets.
    It is ment to be used with the OverseerStrategy
    """
    def __init__(self, strategy, name, cltr=None):
        Player.__init__(self, strategy, name, cltr)
        self.__i = '-'


    def play(self):
        self.bet_size = self.strategy.get_bet_size()
        self.bet_choice = self.strategy.get_bet_choice()
        self.bet(self.bet_size)

    def submit_data(self):
        data = [self.bet_choice, '--', '--', self.bet_size,
                self.res, self.statistics['net']]
        self.cltr.push_player_data(self.name, data)