from abc import ABCMeta, abstractmethod
from random import randint


def roll():
    n = randint(0, 1)  # player : bank ratio is not exactly 50:50!
    if n == 1:
        return 'player'
    else:
        return 'bank'


class Game:
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


    def remove(self, gambler):
        self.gamblers.remove(gambler)

    def submit_data(self):
        self.cltr.push_game_data([self.round, self.outcome])

    def run(self, rounds):
        self.max_rounds = rounds
        while self.gamblers and self.round <= self.max_rounds:
            self.deal()

    def set_outcome(self, outcome=None):

        if outcome:
            self.outcome = outcome
        else:
            self.outcome = self.roll()

        self.notify_observers()

        if self.cltr:
            self.submit_data()  # TODO: decentralize submit_data (submit each value from where it should be submitted)

    def deal(self):
        self.round += 1
        for gambler in self.gamblers:
            gambler.play()

    def notify_observers(self):
        assert self.outcome is not None

        for gambler in self.gamblers:
            if gambler.bet_choice == self.outcome:
                if self.outcome == 'player':
                    amount = gambler.bet_size * 2
                else:
                    amount = gambler.bet_size * 1.95
                gambler.update(outcome='win', reward=amount)
            else:
                gambler.update(outcome='loss')


class BasePlayer:
    __metaclass__ = ABCMeta

    def __init__(self, strategy, name, cltr=None):
        self.cltr = cltr
        self.name = name
        self.strategy = strategy
        self.bet_size = 0
        self.bet_choice = None
        self.statistics = {'net': 0, 'won': 0, 'lost': 0, 'largest_bet': 0}
        self.res = 'loss'
        self.table = None

    def submit_data(self, pre_result=True):

        try:
            partner = self.strategy.pair.name
        except AttributeError:
            partner = '--'

        try:
            target = round(self.strategy.level_target, 2)
        except AttributeError:
            target = '--'

        try:
            level = self.strategy.level
        except AttributeError:
            level = '--'

        try:
            index = self.strategy.i
        except AttributeError:
            index = '--'

        try:
            bet = str(self.bet_size) if not self.strategy.double_up else '2*' + str(self.bet_size / 2)
        except AttributeError:
            bet = str(self.bet_size)

        if pre_result:
            data = [partner, self.bet_choice, level, index, bet, '--', '--', '--']
            self.cltr.push_player_data(self.name, data)
        else:
            data = [partner, self.bet_choice, level, index, bet, self.res, target, self.statistics['net']]

            self.cltr.push_player_data(self.name, data, append=False)

    @abstractmethod
    def update(self, outcome, reward=None):
        """Must be implemented in a concrete subclass"""

    def join(self, table):
        table.add(self)
        self.table = table

    def bet(self, amount):
        if amount > self.statistics['largest_bet']:
            self.statistics['largest_bet'] = amount

        self.statistics['net'] = round(self.statistics['net'] - amount, 2)

    def play(self):
        self.bet_size = self.strategy.get_bet_size()
        self.bet_choice = self.strategy.get_bet_choice()  # (1) after this moment we have (bet_size, bet_choice)
        assert self.bet_size is not None
        assert self.bet_choice is not None

        if self.cltr:
            self.submit_data(pre_result=True)
        self.bet(self.bet_size)


class Player(BasePlayer):

    def update(self, outcome, reward=None):
        self.res = outcome
        if reward:
            self.statistics['won'] += 1
            assert reward is not None
            self.statistics['net'] = round(self.statistics['net'] + reward, 2)
        else:
            self.statistics['lost'] += 1

        try:
            self.strategy.update_level_target(reward)
        except AttributeError:
            print('ERRORRORORROR')

        if self.cltr:
            self.submit_data(pre_result=False)

        self.strategy.update(outcome)


class Overseer(BasePlayer):
    """
    This class represents a player that calculates bets depending on the other players bets.
    It is meant to be used with the OverseerStrategy
    """
    def __init__(self, strategy, name, cltr=None):
        BasePlayer.__init__(self, strategy, name, cltr)

    def update(self, outcome, reward=None):
        self.res = outcome
        if reward:
            self.statistics['won'] += 1
            assert reward is not None
            self.statistics['net'] = round(self.statistics['net'] + reward, 2)
        else:
            self.statistics['lost'] += 1

        if self.cltr:
            self.submit_data(pre_result=False)


