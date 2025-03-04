import numpy as np
from src.utils import dir_to_point
from src.constants import LEFT, RIGHT, UP, DOWN, \
    REWARD_MAP, DEAD, EMPTY, WALL, TAIL


def game_state(grid):
    board = grid.get_board()
    x, y = grid.get_head_pos()

    grid_size = grid.get_grid_size()
    state = [
        next_obj_in_dir(grid, LEFT),
        next_obj_in_dir(grid, RIGHT),
        next_obj_in_dir(grid, UP),
        next_obj_in_dir(grid, DOWN),
        close_to_death(x, y, LEFT, board, grid_size),
        close_to_death(x, y, RIGHT, board, grid_size),
        close_to_death(x, y, UP, board, grid_size),
        close_to_death(x, y, DOWN, board, grid_size),
        grid.get_current_dir() == LEFT,
        grid.get_current_dir() == RIGHT,
        grid.get_current_dir() == UP,
        grid.get_current_dir() == DOWN
    ]
    return np.array(state, dtype=int)


def get_reward(new_case):
    return REWARD_MAP[new_case]


def step(action, grid):
    new_case = EMPTY
    if action == 0 and grid.get_current_dir() != DOWN:
        new_case = grid.update_board(UP)
    elif action == 1 and grid.get_current_dir() != UP:
        new_case = grid.update_board(DOWN)
    elif action == 2 and grid.get_current_dir() != RIGHT:
        new_case = grid.update_board(LEFT)
    elif action == 3 and grid.get_current_dir() != LEFT:
        new_case = grid.update_board(RIGHT)
    else:
        new_case = grid.update_board(grid.get_current_dir())

    return get_reward(new_case), (True if new_case == DEAD else False)


def is_obj_in_dir(grid, dir, obj):
    x, y = grid.get_head_pos()

    obj_pos = np.argwhere(grid.get_board() == obj)
    x_dir, y_dir = dir_to_point(dir)
    for pos in obj_pos:
        x_obj, y_obj = pos
        diff_x = x_obj - x
        diff_y = y_obj - y
        if x + x_dir * diff_x == x_obj and y + y_dir * diff_y == y_obj:
            return True
    return False


def next_obj_in_dir(grid, dir):
    x, y = grid.get_head_pos()
    size = grid.get_grid_size()
    board = grid.get_board()
    x_dir, y_dir = dir_to_point(dir)

    x += x_dir
    y += y_dir

    while 0 < x < size and 0 < y < size:
        if board[x, y] != EMPTY:
            return board[x, y] - 1
        x += x_dir
        y += y_dir
    return WALL - 1


def close_to_death(x, y, dir, board, grid_size):
    x_dir, y_dir = dir_to_point(dir)
    next_x = x + x_dir
    next_y = y + y_dir

    if next_x < 0 or next_x >= grid_size or next_y < 0 or next_y >= grid_size:
        return True

    if board[next_x, next_y] == WALL:
        return True
    if board[next_x, next_y] == TAIL:
        return True
    return False
