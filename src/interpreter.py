import numpy as np
from src.constants import LEFT, RIGHT, UP, DOWN, REWARD_MAP, DEAD, EMPTY, WALL


def game_state(grid):
    board = grid.get_board()
    x, y = grid.get_head_pos()

    every_direction = np.empty((4, grid.get_grid_size()))
    every_direction[0] = np.concatenate((board[x, :y], [WALL] * (grid.get_grid_size() - y)))
    every_direction[1] = np.concatenate((board[x, y:], [WALL] * (y)))
    every_direction[2] = np.concatenate((board[:x, y], [WALL] * (grid.get_grid_size() - x)))
    every_direction[3] = np.concatenate((board[x:, y], [WALL] * (x)))
    return every_direction


def get_reward(new_case):
    return REWARD_MAP[new_case]


def step(action, grid):
    new_case = EMPTY
    if action == 0:
        new_case = grid.update_board(LEFT)
    elif action == 1:
        new_case = grid.update_board(RIGHT)
    elif action == 2:
        new_case = grid.update_board(UP)
    elif action == 3:
        new_case = grid.update_board(DOWN)

    return get_reward(new_case), (True if new_case == DEAD else False)
