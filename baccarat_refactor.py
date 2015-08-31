
from random import randint


def roll():
    n = randint(0, 1)
    if n == 1:
        return 'player'
    else:
        return 'bank'

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

    def register(gamblers):  # player objects
        self.gamblers = []
        self.outcome = None
        self.gamblers = gamblers
        self.play()
        self.update()

    def play():
        self.outcome = self.roll()

    def update():
        assert self.outcome is not None
        
        for gambler in self.gamblers:
            if gambler.bet == self.outcome:
                gambler.update('win')
            else:
                gambler.update('loss')


class BaseStrategy():
    def __init__(self):
        #           0  1  2  3  4  5  6   7   8   9
        # self.row = [2, 2, 2, 4, 4, 8, 12, 20, 32, 52]
        self.row = [1, 1, 1, 2, 2, 4, 6, 10, 16, 26]
        self.i = 0  # row index position
        self.double_up = False
        self.last_index = -1  # ??
        self.level = 1
        self.level_target = 0 # drop to lower level after this gets to (sum(self.row) * level ) / 2


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

        if (self.i <= 2 or self.i == 4) and self.last_index == self.i and self.double_up == False:
            # if self.last_index == self.i and self.double_up == False:  # if double_up was False till now
                self.double_up = True
        elif self.double_up == True:  # if double_up was True till now
                self.double_up = False


    def get_bet_size(self):  # res - result
        bet = 0
        self.is_double()
        level_multiplier = 2 ** (self.level - 1)
        if self.double_up:
            bet = self.row[self.i] * level_multiplier * 2  # or make double_up int (1 or 2) and multiply by it
        else:
            bet = self.row[self.i] * level_multiplier

        self.last_index = self.i
        assert bet > 0
        return bet



class Player():
    def __init__(self, strategy):
        self.strategy = strategy
        self.net = 0
        self.res = 'l'
        self.won = 0
        self.lost = 0
        self.largest_bet = 0

    def bet (self, amount):
        if amount > self.largest_bet:
            self.largest_bet = amount
        self.net -= amount
        self.strategy.level_target -= amount

        outcome = roll()
        if outcome == 'p':
            self.res = 'w'
            self.net += 2 * amount
            self.won += 1
            self.strategy.level_target += 2 * amount
            self.strategy.update_level()
        else:
            self.res = 'l'
            self.lost += 1

        print('{:>3} {:>6} {:>4} {:>3} {:>3} {:>6}'.format(
                        self.strategy.i,
                        str(self.strategy.double_up), 
                        amount,
                        self.strategy.level,
                        self.res,
                        self.net))

        self.strategy.update_index(self.res)


    def play(self, num_hands):
        for i in range(num_hands):
            bet_amount = self.strategy.get_bet_size()
            self.bet(bet_amount)
            

            

strat = BaseStrategy()
p1 = Player(strat)

print('{:>3} {:>6} {:>4} {:>3} {:>3} {:>6}'.format(
                'i',
                'd_up',
                'bet',
                'level',
                'res',
                'net'))
p1.play(1000000)


print('Statistics:')
print('plays won:   ', p1.won)
print('plays lost:  ', p1.lost)
print('largest bet: ', p1.largest_bet)
