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

    def __len__(self):
        return len(self.body)

    def reset(self):

        if self.player == 1:
            self.body = [((self.n - 1, 0), "U")]
        elif self.player == 2:
            self.body = [((self.n - 1, self.n - 1), "U")]

    def change_direction(self, new_direction):
        old_direction = self.body[0][1]
        bad_direction = {"U": "D", "D": "U", "L": "R", "R": "L"}[old_direction]

        assert new_direction != bad_direction

        self.body[0] = (self.body[0][0], new_direction)

    def ixs(self):
        return [ix for ix, _direction in self.body]

    def new_ix(self, ix, direction):
        new_ix = {
            "U": (lambda x: (x[0] - 1, x[1])),
            "D": (lambda x: (x[0] + 1, x[1])),
            "L": (lambda x: (x[0], x[1] - 1)),
            "R": (lambda x: (x[0], x[1] + 1)),
        }[direction](ix)
        return new_ix

    def new_head_ix(self):
        ix, direction = self.body[0]
        return self.new_ix(ix, direction)

    def next_ixs(self, fruit_ix):
        """Returns the next set of ixs, will crash if not possible"""
        if self.new_head_ix() == fruit_ix:
            return [self.new_head_ix()] + self.ixs()
        else:
            return [self.new_head_ix()] + self.ixs()[:-1]

    def step_result(self):
        """Returns "Okay" or "Wall_collision"."""
        new_head_ix = self.new_head_ix()
        if new_head_ix[0] not in range(self.n) or new_head_ix[1] not in range(self.n):
            return "Wall_collision"
        else:
            return "Okay"

    def step(self, fruit_ix):
        assert self.step_result() == "Okay"
        new_head_ix = self.new_head_ix()
        new_pair = (new_head_ix, self.body[0][1])

        if new_head_ix == fruit_ix:
            self.body = [new_pair] + self.body
        else:
            self.body = [new_pair] + self.body[:-1]

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

    def step_results(self):
        step_results = {}
        next_ixs = {}

        for snake in self.snakes:
            step_result = snake.step_result()
            assert step_result in ["Okay", "Wall_collision"]

            step_results[snake.player] = step_result
            next_ixs[snake.player] = snake.next_ixs(self.fruit_ix)

        for player, other_player in zip([1, 2], [2, 1]):
            if step_results[player] == "Okay":
                head_ix = next_ixs[player][0]
                other_ixs = next_ixs[other_player]

                if head_ix in other_ixs:
                    # A head on head collision will be a draw (both lose)
                    step_results[player] = "Snake_collision"

        return step_results

    def okay_to_step(self):
        return self.step_results() == {1: "Okay", 2: "Okay"}

    def step(self):

        # Ensure that no snakes are going to collide with the wall or each other
        assert self.okay_to_step()

        fruit_eaten = False
        for snake in self.snakes:
            old_len = len(snake)
            snake.step(self.fruit_ix)
            if len(snake) > old_len:
                fruit_eaten = True

        if fruit_eaten:
            self.fruit_ix = None
            self.add_fruit()

    def image_str(self):
        image_str = np.full((self.n, self.n), " ")

        if self.fruit_ix is not None:
            image_str[self.fruit_ix] = "*"

        for snake in self.snakes:
            for ix, direction in snake.body:
                image_str[ix] = {"U": "^", "D": "v", "L": "<", "R": ">"}[direction]

        image_str = (
            ("." * (self.n + 2) + "\n")
            + "".join("." + "".join(x for x in line) + ".\n" for line in image_str)
            + ("." * (self.n + 2) + "\n")
        )

        return image_str

    def print(self):
        for snake in self.snakes:
            snake.print()

        print("Fruit: ", self.fruit_ix)

        print(self.image_str())


class Player(object):
    """A player on an n x n game of snake"""

    def __init__(self, n, policy):
        """[policy] is a function from a board state to a move ("U", "D", "L", "R")"""
        self.n = n

        self.policy = policy

    def execute_policy(self, board, player):
        assert player in [1, 2]

        next_direction = self.policy(board)
        assert next_direction in ["U", "D", "L", "R"]

        board.snakes[player - 1].change_direction(next_direction)


class Game(object):
    def __init__(self, n, player1, player2):
        self.n = n
        self.player1 = player1
        self.player2 = player2

        self.board = Board(n)

    def play(self):
        self.board.reset()

        self.board.print()
        while self.board.okay_to_step():

            self.player1.execute_policy(self.board, 1)
            self.player2.execute_policy(self.board, 2)

            self.board.print()
            self.board.step()
            self.board.print()

        step_results = self.board.step_results()
        print(step_results)

        if step_results[1] == "Okay" and step_results[2] != "Okay":
            print("Player 1 wins")
        elif step_results[2] == "Okay" and step_results[1] != "Okay":
            print("Player 2 wins")
        else:
            print("Draw")
