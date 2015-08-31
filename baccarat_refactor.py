
from random import randint


class Game():
    def __init__(self):
        self.gamblers = []
        self.outcome = None

    def roll():
        n = randint(0, 1)  # player : bank ratio is not exactly 50:50!
        if n == 1:
            return 'player'
        else:
            return 'bank'

    def register(self, gamblers):  # player objects
        self.gamblers = gamblers
        self.run()

    def run(self):
        for gambler in self.gamblers:
            # gambler.play()
        self.outcome = self.roll()
        self.notify_observers()

    def notify_observers(self):
        assert self.outcome is not None

        for gambler in self.gamblers:
            if gambler.bet_choice == self.outcome:
                gambler.update(outcome = 'win', reward = 0)
            else:
                gambler.update(outcome = 'loss')


class BaseStrategy():
    def __init__(self, coefficient = 1):
        base_row = [1, 1, 1, 2, 2, 4, 6, 10, 16, 26]
        self.c = coefficient
        self.row = [i*c for i in base_row]
        self.i = 0
        self.double_up = False
        self.outcome = 'loss'
        self.level = 1
        self.level_target = 0 # drop to lower level after this gets to (sum(self.row) * level ) / 2

    def update(self, outcome, reward = None):
        self.outcome = outcome
        if reward:
            self.level_target += reward
            self.update_level()

            
    def update_level(self, increase = False):
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
    
    def update_index(self, last_outcome):
        
        if last_outcome == 'l':
            self.i += 1
        elif self.i == 3 or self.i >= 5:
            self.i -= 3
        else:  # if self.i <= 2 or self.i == 4 AND last_outcome == 'w'
            if self.double_up:
                self.i = 0  # this is after we've played double bet and won -> we must go to 0

        if self.i >= len(self.row):  # if we loose all go to [0] 
            self.i = 0
            self.update_level(increase = True)
            # self.level += 1  # or self.level *= 2 ... linear or geomethric
        assert 0 <= self.i < len(self.row)


    def is_double(self):
        # self.double_up is going to be used in THIS play
        if (self.i <= 2 or self.i == 4) and self.outcome == 'win' and self.double_up == False:
                self.double_up = True
        elif self.double_up == True:  # if double_up was True till now
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

    def get_bet_choice(self):
        return 'player'



class Player():
    def __init__(self, strategy):
        self.strategy = strategy
        self.bet_size = None
        self.bet_choice = None
        self.statistics = {'net' : 0, 'won' : 0, 'lost' : 0, 'largest_bet' : 0}
        self.res = 'l'

    def update (self, outcome, reward = None):
        self.strategy.update(outcome)
        self.res = outcome

        if reward:
            self.statistics['won'] += 1
            assert reward is not None
            self.net += reward
        else:
            self.statistics['lost'] += 1

    def bet (self, amount):
        if amount > self.statistics['largest_bet']
            self.statistics['largest_bet'] = amount

        self.statistics['net'] -= amount
        self.strategy.level_target -= amount  # move to strategy


        print('{:>3} {:>6} {:>4} {:>3} {:>3} {:>6}'.format(
                        self.strategy.i,
                        str(self.strategy.double_up), 
                        amount,
                        self.strategy.level,
                        self.res,
                        self.net))

    def play(self):
        self.bet_size = self.strategy.get_bet_size()
        self.bet_choice = self.strategy.get_bet_choice()
        self.bet(self.bet_size, self.bet_choice)
            

            

strat = BaseStrategy()
p1 = Player(strat)


print('{:>3} {:>6} {:>4} {:>3} {:>3} {:>6}'.format(
                'i',
                'd_up',
                'bet',
                'level',
                'res',
                'net'))



print('Statistics:')
print('plays won:   ', p1.won)
print('plays lost:  ', p1.lost)
print('largest bet: ', p1.largest_bet)
