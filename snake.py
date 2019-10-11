import itertools
import numpy as np


class Snake(object):
    # TODO describe the encoding
    """A snake on a board of size n x n"""

    def __init__(self, n, player):
        assert player in [1, 2]

        self.n = n
        self.player = player
        self.body = []

    def reset(self):

        if self.player == 1:
            self.body = [((self.n - 1, 0), "U")]
        elif self.player == 2:
            self.body = [((self.n - 1, self.n - 1), "U")]

    def ixs(self):
        return [ix for ix, _direction in self.body]

    def print(self):
        print("Snake: ", self.player)
        print(self.body)


class Board(object):
    """A snake board of size n x n"""

    def __init__(self, n):
        self.n = n

        self.snake1 = Snake(n, 1)

        self.snake2 = Snake(n, 2)

        self.snakes = [self.snake1, self.snake2]

        self.fruit_ix = None

    def ixs(self):
        return list(itertools.product(range(self.n), range(self.n)))

    def empty_ixs(self):
        empty_ixs = self.ixs()

        for snake in self.snakes:
            for ix in snake.ixs():
                if ix in empty_ixs:
                    empty_ixs.remove(ix)

        if self.fruit_ix is not None:
            if self.fruit_ix in empty_ixs:
                empty_ixs.remove(self.fruit_ix)

        return empty_ixs

    def add_fruit(self):
        assert self.fruit_ix is None

        empty_ixs = self.empty_ixs()
        i = np.random.choice(range(len(empty_ixs)))

        self.fruit_ix = empty_ixs[i]

    def reset(self):

        for snake in self.snakes:
            snake.reset()

        self.add_fruit()

    def print(self):
        for snake in self.snakes:
            snake.print()

        print("Fruit: ", self.fruit_ix)
