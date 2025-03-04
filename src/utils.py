import pygame
import numpy as np
import matplotlib.pyplot as plt
from src.constants import UP, DOWN, LEFT, RIGHT, \
    CHAR_MAP, MODELS_PATH, SUB_PLOT_STEPS
import os
from natsort import natsorted


def last_trained_model():
    models = os.listdir(MODELS_PATH)
    if len(models) == 0:
        return None
    last_model = os.path.join(MODELS_PATH, natsorted(models)[-1])
    print(f"Last trained model: {last_model}")
    return last_model


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


def dir_from_keys(keys, grid):
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
    return next_dir


def convert_vec_to_str(vec):
    str_list = [CHAR_MAP[val] for val in vec]
    return ''.join(str_list)


def snake_vision(grid):
    board = grid.get_board()
    x, y = grid.get_head_pos()
    return np.concatenate((board[x, :], board[:, y]))


def print_snake_vision(grid):
    vision = snake_vision(grid)
    grid_size = grid.get_grid_size()
    x, y = grid.get_head_pos()

    str_grid = np.full((grid_size, grid_size), ' ', dtype=list)

    row_str = convert_vec_to_str(vision[:grid_size])
    col_str = convert_vec_to_str(vision[grid_size:])

    str_grid[x, :] = list(row_str)
    str_grid[:, y] = list(col_str)

    print("\n".join("".join(row) for row in str_grid))


def analyse_scores(scores):
    if len(scores) == 0:
        return
    print(f"Max score: {max(scores)}")
    print(f"Min score: {min(scores)}")
    print(f"Mean score: {sum(scores) / len(scores):.2f}")
    print(f"Standard deviation: {np.std(scores):.2f}")
    print(f"Number of epochs: {len(scores)}")
    print()


def display_learning_curve(scores):
    # keep n points used to create a curve with less points
    recuded_scores = []
    for i in range(0, len(scores), SUB_PLOT_STEPS):
        recuded_scores.append(np.mean(scores[i:i + SUB_PLOT_STEPS]))
    plt.plot(range(len(scores)), scores)
    plt.plot(range(0, len(scores), SUB_PLOT_STEPS), recuded_scores, 'r')
    plt.xlabel("Epochs")
    plt.ylabel("Scores")
    plt.title("Learning Curve")
    plt.show()
