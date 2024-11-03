import pygame
import numpy as np
from src.constants import UP, DOWN, LEFT, RIGHT, CHAR_MAP


def dir_to_point(dir):
    if dir is None:
        return np.array([0, 0])

    if dir == UP:
        return np.array([-1, 0])
    elif dir == DOWN:
        return np.array([1, 0])
    elif dir == LEFT:
        return np.array([0, -1])
    elif dir == RIGHT:
        return np.array([0, 1])
    else:
        return np.array([0, 0])


def handle_keys(keys, grid):
    current_dir = grid.get_current_dir()
    next_dir = grid.get_current_dir()

    if (keys[pygame.K_z] or keys[pygame.K_UP]) and current_dir != DOWN:
        next_dir = UP
    elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and current_dir != UP:
        next_dir = DOWN
    elif (keys[pygame.K_q] or keys[pygame.K_LEFT]) and current_dir != RIGHT:
        next_dir = LEFT
    elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and current_dir != LEFT:
        next_dir = RIGHT
    elif keys[pygame.K_ESCAPE]:
        return False

    grid.update_board(next_dir)
    return True


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
