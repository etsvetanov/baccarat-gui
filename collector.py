__author__ = 'evgeni'
from collections import defaultdict


class Collector():
    def __init__(self):
        self.player_data = defaultdict(list)
        self.game_data = []

    def push_player_data(self, name, data):
        """
        :param name: name of the player
        :param data: the data itself
        :return:
        """
        self.player_data[name].append(data)

    def push_game_data(self, outcome):
        self.game_data.append(outcome)
