import enum
from collections import namedtuple


class Player(enum.Enum):
    '''
    A player can be either white or black.
    After a player places a stone, you can switch,
    the color by calling the other method on a Player instance
    '''
    x = 1 # If running Player(1) you get returned Player.black
    o = 2

    @property
    def other(self):
        return Player.x if self == Player.o else Player.o


class Point(namedtuple('Point','col row')):

    '''
    We want to represent coordinates on the board using tuples.
    A namedtuple lets you access the coordinates as point.row and point.col
    instead of point[0] and point[1]
    '''

    def neighbors(self):

        return [
            Point(self.col - 1, self.row),
            Point(self.col + 1, self.row),
            Point(self.col, self.row - 1),
            Point(self.col - 1, self.row - 1),
            Point(self.col + 1, self.row - 1),
        ]