from core import *
from data_visualization import *
from strategies import PairStrategy, OverseerStrategy


class GameFactory:
    def __init__(self, num_p, multiplier, starting_bet):
        self.num_p = num_p
        self.multiplier = multiplier
        self.starting_bet = starting_bet

    def create(self, columns):
        players = []
        collector = Collector(columns)
        for i in range(self.num_p):
            strategy_a = PairStrategy(coefficient=self.starting_bet, base=self.multiplier)

            p1 = Player(strategy=strategy_a, name='P' + str(i*2 + 1), cltr=collector)

            strategy_b = PairStrategy(coefficient=self.starting_bet, base=self.multiplier)
            p2 = Player(strategy=strategy_b, name='P' + str(i*2 + 2), cltr=collector)

            p1.strategy.set_pair(p2)
            p2.strategy.set_pair(p1)
            players.append(p1)
            players.append(p2)

        overseer_strat = OverseerStrategy(minions=players)
        overseer = Overseer(strategy=overseer_strat, name='RealPlayer', cltr=collector)

        tbl = Game(cltr=collector, gamblers=players + [overseer], max_rounds=100000)

        return collector, tbl  # tbl is a game table (as in where players sit), i.e. the game object
