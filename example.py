import snake
import numpy as np


def policy1(board):
    return np.random.choice(["U", "R"])


def policy2(board):
    return np.random.choice(["U", "L"])


n = 10

player1 = snake.Player(n, policy1)
player2 = snake.Player(n, policy2)

game = snake.Game(n, player1, player2)
for i in range(n + 2):
    game.step()
