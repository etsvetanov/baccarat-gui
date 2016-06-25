from abc import ABCMeta, abstractmethod

from core import roll


REGISTRY = {}

def registerStrategy(cls):
    REGISTRY[cls.__name__] = cls
    return cls


class BaseStrategy:
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def get_description():
        """returns the strategy description"""

    @abstractmethod
    def get_bet_choice(self):
        """ returns 'player' or 'bank' """

    @abstractmethod
    def get_bet_size(self):
        """ returns bet size """


# noinspection PyMethodOverriding
@registerStrategy
class SingleStrategy(BaseStrategy):
    def __init__(self, coefficient=1, base=2):
        base_row = [1, 1, 1, 2, 2, 4, 6, 10, 16, 26]
        self.c = coefficient
        self.row = [i * self.c for i in base_row]
        self.i = 0
        self.double_up = False
        self.outcome = 'loss'
        self.level = 1
        self.level_target = 0  # drop to lower level after this gets to (sum(self.row) * level ) / 2
        self.last_index = 0
        self.base = base

    @staticmethod
    def get_description():
        description = ("A strategy consisting of a single player. The player bets randomly "
        "on bank or player. The bet ammount follows the betting steps.")

        return description

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
        level_multiplier = self.base ** (self.level - 1)

        if self.double_up:
            bet = self.row[self.i] * level_multiplier * 2  # or make double_up int and multiply by it
        else:
            bet = self.row[self.i] * level_multiplier

        assert bet > 0
        self.level_target -= bet

        return round(bet, 1)

    @staticmethod
    def get_bet_choice():
        choice = roll()
        return choice


# noinspection PyMethodOverriding
@registerStrategy
class PairStrategy(SingleStrategy):
    def __init__(self, coefficient=1, base=2):
        SingleStrategy.__init__(self, coefficient, base)
        self.lead = False
        self.pair = None

    @staticmethod
    def get_description():
        description = ("A strategy that consists of two players each betting amount "
        "that follows the betting steps. One of the players bets randomly on bank or player "
        "and the other one always bets the opposite.")

        return description

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

    def update_level_target(self, reward=None):
        if reward:
            self.level_target += reward
            self.pair.strategy.level_target += reward
            self.update_level()

    def update(self, outcome):
        self.outcome = outcome
        self.update_index()
        self.is_double()

    def get_bet_size(self):  # res - result
        level_multiplier = self.base ** (self.level - 1)

        if self.double_up:
            bet = self.row[self.i] * level_multiplier * 2  # or make double_up int and multiply by it
        else:
            bet = self.row[self.i] * level_multiplier

        assert bet > 0
        self.level_target -= bet
        self.pair.strategy.level_target -= bet

        return round(bet, 1)

    def update_level(self, increase=False):
        """
        go to a higher level if you loose the last
         bet in the row
        or go to level 0 if you win back the cumulative amount lost
        :param increase: player level is increased when True
        """
        if increase:
            self.level += 1
            self.pair.strategy.level += 1
        elif self.level_target > 0:  # TODO: also check if level > 1 then reset both players indexes to 0
            self.level = 1
            self.level_target = 0
            self.pair.strategy.level = 1
            self.pair.strategy.level_target = 0

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
            self.pair.strategy.i = 0
            self.update_level(increase=True)
            # self.level += 1  # or self.level *= 2 ... linear or geometric
        assert 0 <= self.i < len(self.row)


# noinspection PyMethodOverriding
@registerStrategy
class OverseerStrategy(BaseStrategy):
    """
    This strategy is ment to be used on the Overseer class
    """
    def __init__(self, minions=None):
        self.minions = minions
        self.calculated = False
        self.bet_size = 0
        self.bet_choice = None
        """ the following are used only for filling data """
        # self.last_index = '-'
        # self.level = '-'

    @staticmethod
    def get_description():
        description = ("Strategy with multiple \"virtual\" players and a single \"real\" player "
        "All the \"virtual\" players are in pairs (each pair uses the PairStrategy). The betting "
        "in the game is done only by the real player - bank or player bet is chosen by the larger "
        "sum of all \"virtual\" players that bet on bank or player. The difference between the sums "
        "is the bet amount.")

        return description

    def calculate(self):
        minion_bets = {'player': 0, 'bank': 0}
        for minion in self.minions:
            # minion_bets[minion.bet_choice] += minion.bet_size
            minion_bets[minion.bet_choice] = round(minion_bets[minion.bet_choice] + minion.bet_size, 2)

        if minion_bets['player'] > minion_bets['bank']:
            self.bet_size, self.bet_choice = minion_bets['player'] - minion_bets['bank'], 'player'
        elif minion_bets['bank'] > minion_bets['player']:
            self.bet_size, self.bet_choice = minion_bets['bank'] - minion_bets['player'], 'bank'
        else:
            self.bet_size, self.bet_choice = 0, 'tie'

        # these are to prevent bugs where 'player' or 'bank' choice is calculated
        # but the bet_size is 0 (if it's 0 it must be a 'tie')
        if self.bet_choice == 'player' and self.bet_size == 0:
            raise NameError('lol this is name error, sure')

        if self.bet_choice == 'bank' and self.bet_size == 0:
            raise NameError('another name error, trolol')


    def get_bet_choice(self):
        if self.calculated:
            self.calculated = False
        else:
            self.calculate()
            self.calculated = True

        return self.bet_choice


    def get_bet_size(self):
        if self.calculated:
            self.calculated = False
        else:
            self.calculate()
            self.calculated = True

        return round(self.bet_size, 1)


@registerStrategy
class OverseerStrategy2(BaseStrategy):
    def __init__(self, minions=None, starting_choice="Bank"):
        self.minions = minions
        self.bet_size = 0
        self.bet_choice = starting_choice


    @staticmethod
    def get_description():
        description = ("A strategy with many virtual players (minions) and a real (overseer) player."
                       "The overseer bet_size is the difference of the minions' 'bank'/'player' bet sums."
                       "The overseer bet_choice follows the pattern XY XY XY ... where X is the starting_choice:"
                       "either Bank or Player")

        return description

    def get_bet_size(self):
        minion_bets = {'player': 0, 'bank': 0}
        for minion in self.minions:
            minion_bets[minion.bet_choice] = round(minion_bets[minion.bet_choice] + minion.bet_size, 2)

        if minion_bets['player'] > minion_bets['bank']:
            self.bet_size = minion_bets['player'] - minion_bets['bank']
        elif minion_bets['bank'] > minion_bets['player']:
            self.bet_size = minion_bets['bank'] - minion_bets['player']
        else:
            self.bet_size = 0

        return self.bet_size

    def get_bet_choice(self):
        if self.bet_size == 0:
            current_choice = "Tie"
        elif self.bet_choice == "Bank":
            current_choice = self.bet_choice
            self.bet_choice = "Player"
        else:
            current_choice = self.bet_choice
            self.bet_choice = "Bank"

        return current_choice
