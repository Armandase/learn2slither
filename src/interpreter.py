import numpy as np
from src.constants import CHAR_MAP

def snake_vision(grid):
    board = grid.get_board()
    x, y = grid.get_head_pos()
    return np.concatenate((board[x, :], board[:, y]))

def convert_vec_to_str(vec):
    str_list = ['W']
    str_list.extend(CHAR_MAP[val] for val in vec)
    str_list.append('W')
    return ''.join(str_list)


def print_snake_vision(vision, grid):
    grid_size = grid.get_grid_size()
    x, y = grid.get_head_pos()

    str_grid = np.full((grid_size + 2, grid_size + 2), ' ', dtype=list)

    row_str = convert_vec_to_str(vision[:grid_size])
    col_str = convert_vec_to_str(vision[grid_size:])

    str_grid[x, :] = list(row_str)
    str_grid[:, y] = list(col_str)

    print("\n".join("".join(row) for row in str_grid))
