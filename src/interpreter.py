import numpy as np
from src.constants import LEFT, RIGHT, UP, DOWN, REWARD_MAP, DEAD, EMPTY


def game_state(grid):
    board = grid.get_board()
    x, y = grid.get_head_pos()
    if x >= grid.get_grid_size() or x < 0 or y >= grid.get_grid_size() or y < 0:
        test = np.zeros((grid.get_grid_size() * 2))
        print("Test:", test.shape)
        return np.zeros((grid.get_grid_size() * 2))
    caca = np.concatenate((board[x, :], board[:, y]))
    print("Caca: ", caca.shape)
    return np.concatenate((board[x, :], board[:, y]))


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
