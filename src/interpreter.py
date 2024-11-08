import numpy as np
from src.utils import dir_to_point
from src.constants import LEFT, RIGHT, UP, DOWN, \
    REWARD_MAP, DEAD, EMPTY, WALL, GREEN_APPLE, RED_APPLE, TAIL



# def game_state(grid):
#     board = grid.get_board()
#     x, y = grid.get_head_pos()

#     grid_size = grid.get_grid_size()
#     state = [
#         close_to_death(x, y, LEFT, board,grid_size ),
#         close_to_death(x, y, RIGHT, board, grid_size),
#         close_to_death(x, y, UP, board, grid_size),
#         close_to_death(x, y, DOWN, board, grid_size),
#         is_obj_in_dir(grid, LEFT, GREEN_APPLE),
#         is_obj_in_dir(grid, RIGHT, GREEN_APPLE),
#         is_obj_in_dir(grid, UP, GREEN_APPLE),
#         is_obj_in_dir(grid, DOWN, GREEN_APPLE),
#         is_obj_in_dir(grid, LEFT, RED_APPLE),
#         is_obj_in_dir(grid, RIGHT, RED_APPLE),
#         is_obj_in_dir(grid, UP, RED_APPLE),
#         is_obj_in_dir(grid, DOWN, RED_APPLE),
#         grid.get_current_dir() == LEFT,
#         grid.get_current_dir() == RIGHT,
#         grid.get_current_dir() == UP,
#         grid.get_current_dir() == DOWN
#     ]
#     return np.array(state, dtype=int)

def game_state(grid):
    state = np.zeros((3, 3), dtype=int)
    board = grid.get_board()
    head_x, head_y = grid.get_head_pos()

    grid_size = grid.get_grid_size()

    # Set the snake head position
    state[1][1] = 2

    # Set the surrounding cells
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, y = head_x + dx, head_y + dy
        if 0 <= x < grid_size and 0 <= y < grid_size:
            if board[y][x] == 1:
                state[1 + dy][1 + dx] = 1
            elif board[y][x] == 3:
                state[1 + dy][1 + dx] = 3
            elif board[y][x] == 2:
                state[1 + dy][1 + dx] = 2

    return state

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

def close_to_death(x, y, dir, board, grid_size):
    x_dir, y_dir = dir_to_point(dir)
    if x + x_dir < 0 or x + x_dir >= grid_size or y + y_dir < 0 or y + y_dir >= grid_size:
        return True

    if board[x + x_dir, y + y_dir] == WALL:
        return True
    elif board[x + x_dir, y + y_dir] == TAIL:
        return True
    return False
