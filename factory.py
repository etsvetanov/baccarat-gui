from core import *
from data_visualization import *
from strategies import PairStrategy, OverseerStrategy, OverseerStrategy2
from abc import ABCMeta, abstractmethod


class GameFactory:
    def __init__(self, num_p, multiplier, starting_bet):
        self.num_p = num_p
        self.multiplier = multiplier
        self.starting_bet = starting_bet

    def create(self, columns):
        players = []
        collector = Collector(columns)
        # collector = None
        for i in range(self.num_p * 2):
            strategy_a = PairStrategy(coefficient=self.starting_bet, base=self.multiplier)

            p1 = Player(strategy=strategy_a, name='P' + str(i*2 + 1), cltr=collector)

            strategy_b = PairStrategy(coefficient=self.starting_bet, base=self.multiplier)
            p2 = Player(strategy=strategy_b, name='P' + str(i*2 + 2), cltr=collector)

            p1.strategy.set_pair(p2)
            p2.strategy.set_pair(p1)
            players.append(p1)
            players.append(p2)

        overseer_strat1 = OverseerStrategy2(minions=players[:int(len(players)/2)], starting_choice="player")
        overseer_strat2 = OverseerStrategy2(minions=players[int(len(players)/2):], starting_choice="bank")
        overseer1 = Overseer(strategy=overseer_strat1, name='RP1', cltr=collector)
        overseer2 = Overseer(strategy=overseer_strat2, name='RP2', cltr=collector)

        tbl = Game(cltr=collector, gamblers=players + [overseer1, overseer2], max_rounds=100000)

        return collector, tbl  # tbl is a game table (as in where players sit), i.e. the game object


# class AbstractGameFactory:
#     def __init__(self, nump_p, multiplier, starting_bet):
#         pass
#
#     def create(self, columns):
#         pass

